from odoo import http
from odoo.http import request
import logging



_logger = logging.getLogger(__name__)
class BookController(http.Controller):
    @http.route('/registration/<int:id>',type='http', auth='public', website=True)
    def reserve_travel(self, voyage_id):
        customer = request.env.user.partner_id
        requested_seats = 1  # ou à récupérer dynamiquement depuis un formulaire

        travel = request.env['travel'].sudo().browse(voyage_id)

        if travel.nbre_place_reserv + requested_seats > travel.nbre_place_disp:
            return request.render('traffic.connexion_failed_template', {
                'message': "Plus assez de places disponibles pour ce voyage."
            })

        # Réservation sécurisée (si logique critique, faire cela en SQL ou via contraintes)
        travel.nbre_place_reserv += requested_seats

        request.env['booking'].sudo().create({
            'travel_id': travel.id,
            'customer_id': customer.id,
            'nbre_place_reserv': requested_seats
        })

        return request.render('traffic.connexion_success_confirmation', {
            'travel': travel,
            'customer': customer,
            'nbre_place_disp': requested_seats
        })
