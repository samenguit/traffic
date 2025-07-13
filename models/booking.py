from odoo import models, fields, api
from odoo.exceptions import UserError
import logging
import qrcode
import base64
from io import BytesIO

_logger = logging.getLogger(__name__)

class Booking(models.Model):
    _name = 'booking'
    _description = 'travel booking'

    travel_id = fields.Many2one('travel', string='voyage')
    date_reservation = fields.Datetime(string="Date de réservation", default=fields.Datetime.now)
    amount_total = fields.Monetary(string="Montant payé", currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Devise', required=True,
                                  default=lambda self: self.env.company.currency_id)
    driver_id = fields.Many2one('driver',string='chauffeur')
    name = fields.Char('nom')
    cni_number = fields.Char('CNI number')
    nbre_place_reserv = fields.Integer('nombre de place')
    phone = fields.Char('Phone')
    departure = fields.Many2one('city', string="Ville de départ", related='travel_id.departure_city', store=True)
    arrival = fields.Many2one('city', related='travel_id.city_of_arrival', store=True)
    customer_id = fields.Many2one(
        'res.partner',
        string='Client',
        default=lambda self: self.env.user.partner_id.id
    )

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('invoice_sent', 'Facture envoyée'),
        ('paid', 'Payée'),
        ('cancelled', 'Annulée'),
    ], default='draft')

    invoice_id = fields.Many2one('account.move', string="Facture liée")
    email = fields.Char(string="Email")

    qr_code = fields.Text("QR Code", compute='_generate_qr_code', store=False)

    def _generate_qr_code(self):
        for record in self:
            data = f"Réservation: {record.name}, CNI: {record.cni_number}, Tel: {record.phone}"
            qr = qrcode.make(data)
            buffer = BytesIO()
            qr.save(buffer, format='PNG')
            qr_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            record.qr_code = qr_b64








