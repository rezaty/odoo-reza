from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = "hr.employee"
    
    ptkp_id = fields.Many2one('hr.ptkp', 'PTKP', compute='_compute_ptkp', store=True)
    jumlah_tanggungan = fields.Integer('Jumlah Tanggungan', default=0)
    punya_npwp = fields.Boolean('Punya NPWP')
    no_npwp = fields.Char('No. NPWP')
    bpjs_ktk = fields.Boolean('Bpjs Ketenagakerjaan')

    @api.depends('gender', 'marital', 'jumlah_tanggungan')
    def _compute_ptkp(self):
        try:
            record_id = self.env.ref('ab_payroll_pph21.tk0').id
            for x in self:
                if x.gender == 'female' and x.marital == 'married':
                    record_id = x.env.ref('ab_payroll_pph21.tk0').id
                if not x.marital:
                    record_id = x.env.ref('ab_payroll_pph21.tk0').id
                if x.marital == 'single' and x.jumlah_tanggungan == 0:
                    record_id = x.env.ref('ab_payroll_pph21.tk0').id
                if x.marital == 'single' and x.jumlah_tanggungan == 1:
                    record_id = x.env.ref('ab_payroll_pph21.tk1').id
                if x.marital == 'single' and x.jumlah_tanggungan == 2:
                    record_id = x.env.ref('ab_payroll_pph21.tk2').id
                if x.marital == 'single' and x.jumlah_tanggungan >= 3:
                    record_id = x.env.ref('ab_payroll_pph21.tk3').id
                if x.marital == 'married' and x.gender == 'male' and x.jumlah_tanggungan == 0:
                    record_id = x.env.ref('ab_payroll_pph21.k0').id
                if x.marital == 'married' and x.gender == 'male' and x.jumlah_tanggungan == 1:
                    record_id = x.env.ref('ab_payroll_pph21.k1').id
                if x.marital == 'married' and x.gender == 'male' and x.jumlah_tanggungan == 2:
                    record_id = x.env.ref('ab_payroll_pph21.k2').id
                if x.marital == 'married' and x.gender == 'male' and x.jumlah_tanggungan >= 3:
                    record_id = x.env.ref('ab_payroll_pph21.k3').id
                if x.marital == 'widower' and x.jumlah_tanggungan == 0:
                    record_id = x.env.ref('ab_payroll_pph21.tk0').id
                if x.marital == 'widower' and x.jumlah_tanggungan == 1:
                    record_id = x.env.ref('ab_payroll_pph21.tk1').id
                if x.marital == 'widower' and x.jumlah_tanggungan == 2:
                    record_id = x.env.ref('ab_payroll_pph21.tk2').id
                if x.marital == 'widower' and x.jumlah_tanggungan >= 3:
                    record_id = x.env.ref('ab_payroll_pph21.tk3').id
                
                x.ptkp_id = record_id
        
        except Exception as e:
            print(e)
