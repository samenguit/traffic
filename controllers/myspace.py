from datetime import timedelta
from odoo import fields, http
from odoo.http import request

class ReservationController(http.Controller):

    @http.route('/mon_espace', type='http', auth='user', website=True)
    def mon_espace(self, voyage_id=None, **kwargs):
        user = request.env.user
        customer = user.partner_id

        # ⚠️ CORRECTION : virgule manquante entre les 2 conditions
        domain = [('customer_id', '=', customer.id)]
        if voyage_id:
            domain.append(('travel_id', '=', int(voyage_id)))

        reservations = request.env['booking'].sudo().search(domain)

        now_dt = fields.Datetime.context_timestamp(customer, fields.Datetime.now())

        # Marquer les réservations comme annulables ou non
        reservations_with_flag = []
        for res in reservations:
            depart_dt = res.travel_id.date_depart
            if depart_dt:
                depart_dt = fields.Datetime.context_timestamp(res, depart_dt)
                annulable = (depart_dt - now_dt) > timedelta(hours=24)
            else:
                annulable = False

            reservations_with_flag.append({
                'record': res,
                'can_cancel': annulable,
            })

        # ⚠️ CORRECTION : erreur de syntaxe dans la recherche de voyage
        voyage = None
        if voyage_id:
            voyage = request.env['travel'].sudo().browse(int(voyage_id))

        return request.render('traffic.mon_espace_template', {
            'reservations': reservations_with_flag,
            'customer': customer,
            'voyage': voyage,
            'voyage_id': voyage.id if voyage else None,
        })

    @http.route('/cancel_booking/<int:booking_id>', type='http', auth='user', methods=['POST'], website=True, csrf=False)
    def cancel_booking(self, booking_id, **kwargs):
        booking = request.env['booking'].sudo().browse(booking_id)

        if not booking.exists():
            return request.redirect('/mon_espace')

        now = fields.Datetime.context_timestamp(booking, fields.Datetime.now())
        date_depart = booking.travel_id.date_depart
        if date_depart:
            date_depart = fields.Datetime.context_timestamp(booking, date_depart)
            if (date_depart - now).total_seconds() < 86400:
                # Moins de 24h : annulation refusée
                return request.render('traffic.mon_espace_template', {
                    'reservations': [{'record': booking, 'can_cancel': False}],
                    'customer': request.env.user.partner_id,
                    'voyage': booking.travel_id,
                    'voyage_id': booking.travel_id.id,
                    'error': "Annulation impossible moins de 24h avant le départ."
                })

        # Mettre à jour les données
        booking.write({'state': 'draft'})  # ou 'cancel' si tu ajoutes la valeur autorisée

        # Mise à jour des places
        travel = booking.travel_id
        travel.write({
            'nbre_place_disp': travel.nbre_place_disp + booking.nbre_place_reserv,
            'nbre_place_reserv': travel.nbre_place_reserv - booking.nbre_place_reserv,
        })

        return request.redirect('/mon_espace')
