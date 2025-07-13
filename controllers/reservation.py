from odoo import http
from odoo.http import request
import logging
from odoo.exceptions import UserError
from urllib.parse import quote





_logger = logging.getLogger(__name__)
class ReservationController(http.Controller):
    @http.route('/reservation/<int:voyage_id>',type='http', auth='public', website=True)
    def reservation_travel(self, voyage_id):
        return request.render('traffic.reservation_template',{
            'voyage_id' : voyage_id,
        })

    @http.route('/store_reservation', type='http', auth='public', website=True, csrf=False)
    def store_reservation(self, **kw):
        user = request.env.user
        customer = user.partner_id

        voyage_id = kw.get('voyage_id')
        if not voyage_id:
            return request.render('traffic.error_template', {'message': "ID du voyage manquant."})

        try:
            voyage_id = int(voyage_id)
        except ValueError:
            return request.render('traffic.error_template', {'message': "ID du voyage invalide."})

        travel = request.env['travel'].sudo().browse(voyage_id)
        if not travel.exists():
            return request.render('traffic.error_template', {'message': "Voyage introuvable."})

        try:
            nb_reserv = int(kw.get('pl_reserv', 0))
        except (ValueError, TypeError):
            nb_reserv = 0

        if nb_reserv <= 0:
            return request.render('traffic.reservation_template', {
                'voyage_id': voyage_id,
                'error': "Le nombre de places réservées doit être supérieur à zéro."
            })

        if travel.nbre_place_disp < nb_reserv:
            return request.render('traffic.reservation_template', {
                'voyage_id': voyage_id,
                'error': "Il n'y a pas assez de places disponibles."
            })

        name = kw.get('nom') or 'Inconnu'
        cni = kw.get('cni')
        phone = kw.get('phone')


        booking = request.env['booking'].sudo().create({
            'name': name,
            'cni_number': cni,
            'nbre_place_reserv': nb_reserv,
            'phone': phone,
            'travel_id': travel.id,
            'amount_total': travel.travel_price * nb_reserv,
            'customer_id': customer.id,
        })



        from urllib.parse import quote
        url_safe_name = quote(name)

        return request.render('traffic.recap_template', {
            'voyage_id': voyage_id,
            'name': name,
            'voyage': travel,
            'booking': booking,
            'url_safe_name': url_safe_name,
            'cni': cni,
        })

