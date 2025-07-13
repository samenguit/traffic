from odoo import models, fields,api
from odoo.exceptions import UserError


class Payment(models.Model):
    _name = 'payment'
    _description = 'payment'

    phone = fields.Char('Entrer le numero de telephone par lequel le tarif sera prélevé:')
    booking_id=fields.Many2one('booking')