from odoo import models, fields

class Typevoyage(models.Model):
    _name = 'type_voyage'
    _description = 'type voyage'
    _rec_name = 'name'

    name = fields.Char('type de voyage')






