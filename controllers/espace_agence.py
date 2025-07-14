from odoo import http
from odoo.http import request
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

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
            type_name = kw.get('type')  # ici on récupère une chaîne

            if depart_id == arrivee_id:
                return request.render('traffic.error_template', {
                    'error': "La ville de départ et d’arrivée ne peuvent pas être identiques."
                })

            # Combine date + heure
            date_depart = datetime.strptime(f"{date_str} {heure_str}", "%Y-%m-%d %H:%M")
            if date_depart < datetime.now():
                return request.render('traffic.error_template', {
                    'error': "La date de départ ne peut pas être dans le passé."
                })

            # Récupération de l'agence associée à l'utilisateur connecté
            user = request.env.user
            agency = request.env['agency'].sudo().search([('user_id', '=', user.id)], limit=1)
            if not agency:
                return request.render('traffic.error_template', {
                    'error': "Aucune agence n’est liée à votre compte."
                })

            # Récupération de l'objet type_voyage à partir de son nom
            type_obj = request.env['type_voyage'].sudo().search([('name', '=', type_name)], limit=1)
            if not type_obj:
                return request.render('traffic.error_template', {
                    'error': f"Type de voyage « {type_name} » introuvable."
                })

            # Création du voyage
            request.env['travel'].sudo().create({
                'departure_city': depart_id,
                'city_of_arrival': arrivee_id,
                'date_depart': date_depart,
                'heure_depart': heure_str,
                'travel_price': prix,
                'nbre_place_disp': dispo,
                'type_id': type_obj.id,
                'agency_id': agency.id,
            })

            return request.render('traffic.success_template')

        except Exception as e:
            _logger.exception("Erreur lors de la soumission du voyage")
            return request.render('traffic.error_template', {
                'error': f"Une erreur est survenue : {str(e)}"
            })
