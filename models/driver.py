from odoo import models, fields
from odoo.exceptions import UserError


class Driver(models.Model):
    _name = 'driver'
    _description = 'driver'





    phone = fields.Char('Telephone chauffeur')
    user_id = fields.Many2one('res.users', string='Utilisateur associé')
    name = fields.Char('Noms et prenoms')
    permis_scan = fields.Binary(string="Scan permis de conduire")
    permis_filename = fields.Char("Nom fichier permis")

    cni_scan = fields.Binary(string="Scan CNI")
    cni_filename = fields.Char("Nom fichier CNI")

    assurance_scan = fields.Binary(string="Scan assurance")
    assurance_filename = fields.Char("Nom fichier assurance")

    carte_grise_scan = fields.Binary(string="Scan carte grise")
    carte_grise_filename = fields.Char("Nom fichier carte grise")







