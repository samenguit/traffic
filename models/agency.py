from odoo import models, fields

class Agency(models.Model):
    _name = 'agency'
    _description = 'agency name'
    _rec_name = 'name'

    name = fields.Char('Nom agence')
    email = fields.Char('email')
    password = fields.Char('password')
    user_id = fields.Many2one('res.users', string="Utilisateur lié")






