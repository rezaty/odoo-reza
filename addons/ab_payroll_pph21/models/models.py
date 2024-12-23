# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class ab_payroll_pph21(models.Model):
#     _name = 'ab_payroll_pph21.ab_payroll_pph21'
#     _description = 'ab_payroll_pph21.ab_payroll_pph21'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
