from odoo import models, fields, api

class Ptkp(models.Model):
    _name = 'hr.ptkp'

    name = fields.Char('Status')
    tahun = fields.Integer('Tarif/Tahun')