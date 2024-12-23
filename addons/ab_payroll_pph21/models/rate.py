from odoo import models, fields, api

class RatePPh21(models.Model):
    _name = 'rate.pph21'
    _description = 'Rate PPh21'

    seq = fields.Integer(string='Sequence')
    nilai_rate = fields.Float(string='Nilai Rate')
    npwp_rate = fields.Float(string='Punya NPWP Rate', digits=(16,3))
    no_npwp_rate = fields.Float(string='Tidak Punya NPWP Rate', digits=(16,3))