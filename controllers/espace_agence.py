from odoo import http
from odoo.http import request
from datetime import datetime

class Espaceagence(http.Controller):

    @http.route('/espace_agence', type='http', auth='user', website=True)
    def espace_agence(self, **kwargs):
        user = request.env.user
        customer = user.partner_id
        types = request.env['type_voyage'].sudo().search([])
        villes = request.env['city'].sudo().search([])
        return request.render('traffic.planning_template', {
            'customer': customer,
            'types': types,
            'villes': villes
        })

    @http.route('/voyage', type='http', auth='user', website=True, methods=['POST'], csrf=True)
    def voyage_submit(self, **kw):
        try:
            depart_id = int(kw.get('depart'))
            arrivee_id = int(kw.get('arrivee'))
            prix = float(kw.get('prix'))
            dispo = int(kw.get('dispo'))
            date_str = kw.get('date')
            heure_str = kw.get('heure')

            # Combine date + heure
            date_depart = datetime.strptime(f"{date_str} {heure_str}", "%Y-%m-%d %H:%M")

            # Créer le voyage
            request.env['travel'].sudo().create({
                'departure_city': depart_id,
                'city_of_arrival': arrivee_id,
                'date_depart': date_depart,
                'heure_depart': heure_str,
                'travel_price': prix,
                'nbre_place_disp': dispo,
            })

            return request.render('traffic.success_template')
        except Exception as e:
            return request.render('traffic.error_template', {'error': str(e)})
