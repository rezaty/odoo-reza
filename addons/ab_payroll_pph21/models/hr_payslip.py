from odoo import models, fields, api

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def get_nilai_pajak(self, bulan_sisa, tahun, ptkp, employee, pajak_yg_sudah_dibayar, payslip_id, pendaptan_tanpa_bonus):
        pajak = 0
        data, pajak_setahun = self.env['hr.payslip'].get_nilai_pkp(tahun, ptkp, employee, payslip_id)
        data, tanpa_bonus = self.env['hr.payslip'].get_nilai_pkp(pendaptan_tanpa_bonus, ptkp, employee, payslip_id)
        payslip = self.browse(payslip_id)

        if payslip.date_from.month == 12:
            pajak_sebenarnya = abs(pajak_setahun) - abs(pajak_yg_sudah_dibayar)
            return pajak_sebenarnya

        pajak_teratur = tanpa_bonus / 12
        pajak_tidak_teratur = pajak_setahun - tanpa_bonus
        pajak = pajak_teratur + pajak_tidak_teratur

        return pajak

    def get_data_pph(self, a, b, c):
        sql = """
        select
            hpl.amount, hpl.code, hp.id
        from hr_payslip_line hpl
        left join hr_payslip hp on (hp.id = hpl.slip_id)
        where hpl.code in ('PPH21', 'PPH21THR', 'PPH21KMS')
        and date_from BETWEEN '%s-01-01' and '%s'
        and hp.employee_id = %s and hp.state = 'done'
        """ % (a, b, c)
        self.env.cr.execute(sql)
        data_sql = self.env.cr.dictfetchall()
        return data_sql

    def get_data_gross(self, a, b, c):
        sql = """
        select
            hpl.amount, hpl.code, hp.id
        from hr_payslip_line hpl
        left join hr_payslip hp on (hp.id = hpl.slip_id)
        left join hr_salary_rule_category hrc on (hrc.id = hpl.category_id)
        where hrc.code in ('BASIC', 'ALW')
        and date_from BETWEEN '%s-01-01' and '%s'
        and hp.employee_id = %s and hp.state = 'done'
        """ % (a, b, c)
        self.env.cr.execute(sql)
        data_sql = self.env.cr.dictfetchall()
        return data_sql

    def get_nilai_pkp(self, tahun, PTKP_tarf_tahun, employee, payslip_id):
        lapis1 = 0
        lapis2 = 0
        lapis3 = 0
        lapis4 = 0
        payslip = self.browse(payslip_id)
        data = {}
        total = 0
        npwp = employee.punya_npwp

        if tahun >= PTKP_tarf_tahun:
            nilai_pkp = tahun - PTKP_tarf_tahun
            rate = self.env['rate.pph21'].search([], order='seq')

            if rate:
                n = 0
                for x in rate:
                    n += 1
                    lapis = 'lapis%s' % (str(n))

                    if nilai_pkp > x.nilai_rate:
                        nilai_lapis = x.nilai_rate * (x.npwp_rate if npwp else x.no_npwp_rate)
                    else:
                        nilai_lapis = nilai_pkp * (x.npwp_rate if npwp else x.no_npwp_rate)

                    nilai_pkp -= x.nilai_rate
                    data[lapis] = nilai_lapis

                    if nilai_pkp < 0:
                        break

        for x in data:
            total += data[x]

        return data, total

    def compute_pph21(self, pendapatan_saat_ini, allowance, date_from, date_to, employee, payslip_id, pengurang):
        PTKP_tarf_tahun = employee.ptkp_id.tahun
        total_bulan_sebelumnya = 0

        # Mencari Biaya jabatan
        biaya_jabatan = ((pendapatan_saat_ini * 12) + allowance) * 0.05
        if biaya_jabatan > 6000000:
            biaya_jabatan = 6000000

        # Mencari Nilai Seluruh Gaji Pada Periode Ini
        data_pph = self.env['hr.payslip'].get_data_pph(date_from, date_to, employee.id)
        data_bruto = self.env['hr.payslip'].get_data_gross(date_from, date_to, employee.id)

        # Mencari Nilai Pajak yang sudah dibayarkan jika sudah ada
        pajak_yg_sudah_dibayar = 0
        if data_bruto:
            total_bulan_sebelumnya = sum([x['amount'] for x in data_bruto])
        
        if data_pph:
            pajak_yg_sudah_dibayar = sum([x['amount'] for x in data_pph if x['code'] in ('PPH21', 'PPH21THR', 'PPH21KMS')])

        bulan_ke = len(data_bruto or ['empty'])
        bulan_sisa = 13 - bulan_ke
        pensiun = pengurang

        biaya_jabatan_tanpa_allowance = ((pendapatan_saat_ini * 12) * 0.05)
        if biaya_jabatan_tanpa_allowance > 6000000:
            biaya_jabatan_tanpa_allowance = 6000000

        pendapatan_disetahunkan = ((pendapatan_saat_ini) * 12) + allowance
        pendapatan = pendapatan_disetahunkan - (biaya_jabatan) - (pensiun * 12)
        pendaptan_tanpa_bonus = ((pendapatan_saat_ini) * 12) - (biaya_jabatan_tanpa_allowance) - (pensiun * 12)

        result = self.get_nilai_pajak(bulan_sisa, pendapatan, PTKP_tarf_tahun, employee, pajak_yg_sudah_dibayar, payslip_id, pendaptan_tanpa_bonus)
        
        return result