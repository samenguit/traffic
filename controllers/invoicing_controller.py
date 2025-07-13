from odoo import http
from odoo.http import request
from datetime import date



class ReservationFactureController(http.Controller):

    @http.route('/facturation/<int:booking_id>', type='http', auth='user', website=True)
    def generate_invoice(self, booking_id):
        reservation = request.env['booking'].sudo().browse(booking_id)

        if not reservation.exists():
            return "Réservation introuvable."

        partner = reservation.customer_id
        travel = reservation.travel_id
        total = reservation.amount_total

        # Récupérer un produit générique déjà créé
        product = request.env['product.product'].sudo().search([
            ('name', '=', 'Reservation de voyage')
        ], limit=1)
        if not product:
            return "Produit 'Reservation de voyage' introuvable. Veuillez le créer."

        # Créer la facture sans forcer le compte_id
        invoice = request.env['account.move'].sudo().create({
            'move_type': 'out_invoice',
            'partner_id': partner.id,
            'invoice_date': date.today(),
            'invoice_origin': f"Réservation #{reservation.name}",
            'invoice_line_ids': [(0, 0, {
                'product_id': product.id,
                'name': f"Réservation de {reservation.nbre_place_reserv} place(s) — {travel.departure_city.city_name} → {travel.city_of_arrival.city_name}",
                'quantity': reservation.nbre_place_reserv,
                'price_unit': travel.travel_price,
            })],
        })

        # Valider la facture
        invoice.action_post()

        template_id = request.env.ref('account.email_template_edi_invoice').id
        request.env['mail.template'].browse(template_id).send_mail(invoice.id, force_send=True)

        return request.redirect(f'/my/invoices/{invoice.id}')
