from odoo import models, fields
from odoo.exceptions import UserError


class Customer(models.Model):
    _name = 'customer'
    _description = 'customer'

    phone = fields.Char('Telephone')
    email = fields.Char('email')
    cni = fields.Char("Nom fichier CNI")
    password = fields.Char('password')
    user_id = fields.Many2one('res.users', string="Utilisateur lié",ondelete="cascade")
    username = fields.Char('Username')








