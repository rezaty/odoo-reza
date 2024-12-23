# -*- coding: utf-8 -*-
# from odoo import http


# class AbPayrollPph21(http.Controller):
#     @http.route('/ab_payroll_pph21/ab_payroll_pph21', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ab_payroll_pph21/ab_payroll_pph21/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ab_payroll_pph21.listing', {
#             'root': '/ab_payroll_pph21/ab_payroll_pph21',
#             'objects': http.request.env['ab_payroll_pph21.ab_payroll_pph21'].search([]),
#         })

#     @http.route('/ab_payroll_pph21/ab_payroll_pph21/objects/<model("ab_payroll_pph21.ab_payroll_pph21"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ab_payroll_pph21.object', {
#             'object': obj
#         })
