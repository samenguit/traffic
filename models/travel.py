from odoo import models,fields,api
from odoo.exceptions import UserError

class Travel(models.Model):
    _name='travel'
    _description='voyage'


    departure_city=fields.Many2one('city',string='Depart')
    departure_point = fields.Char('Lieu de depart')
    city_of_arrival = fields.Many2one('city', string='Arrivee')
    date_depart = fields.Datetime('date depart')
    heure_depart = fields.Char(string="Heure de départ (HH:MM)")
    nbre_place_disp=fields.Integer('place disponible')
    nbre_place_reserv = fields.Integer('place reserve', readonly=True)
    customer_ids=fields.Many2many('res.partner', string='client')
    type_id =fields.Many2one('type_voyage')
    travel_price = fields.Float('Prix', store=True)
    driver_id = fields.Many2one('res.partner', string='chauffeur')
    agency_id = fields.Many2one('agency', string='agency' )

    reservation_ids = fields.One2many('booking', 'travel_id', string="Réservations")

    driver_name = fields.Char(string='Nom chauffeur', compute='_compute_driver_data', store=True)
    driver_cni = fields.Char(string='CNI chauffeur', compute='_compute_driver_data', store=True)
    driver_phone = fields.Char(string='Telephone', compute='_compute_driver_data', store=True)
    type_name = fields.Char(string='type', compute='_compute_type_data', store=True)

    @api.depends('type_id')
    def _compute_type_data(self):
        for rec in self:
            rec.type_name = rec.type_id.name or ''


    @api.depends('driver_id')
    def _compute_driver_data(self):
        for rec in self:
            rec.driver_name = rec.driver_id.name or ''
            rec.driver_cni = rec.driver_id.cni or ''
            rec.driver_phone = rec.driver_id.phone or ''

    _sql_constraints = [
        ('check_nbre_place_disp_positive',
         'CHECK(nbre_place_disp >= 0)',
         'Le nombre de places disponibles doit être supérieur ou égal à zéro.'),
        ('check_nbre_place_reserv_pos',
         'CHECK(nbre_place_reserv >= 0)',
         'Le nombre de places reserve doit être supérieur ou égal à zéro.')
    ]

    status = fields.Selection(
        selection=[('available', 'disponible'), ('full', 'plein'), ('cancel', 'annuler')],
        compute='_compute_status',
        store=True
    )
    is_cancelled = fields.Boolean(string="Annulé", default=False)

    @api.depends('nbre_place_disp', 'is_cancelled')
    def _compute_status(self):
        for record in self:
            if record.is_cancelled:
                record.status = 'cancel'
            elif record.nbre_place_disp == 0:
                record.status = 'full'
            else:
                record.status = 'available'














