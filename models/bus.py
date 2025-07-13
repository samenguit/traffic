from odoo import models, fields

class Bus(models.Model):
    _name = 'bus'
    _description = 'registration_number'
    _rec_name = 'registration_number'



    mark = fields.Char('marque')
    registration_number = fields.Char('immatriculation')
    insurance_number = fields.Char('numero assurance')
    type = fields.Char('type')
    agency_id = fields.Many2one('agency')



