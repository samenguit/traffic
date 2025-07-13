from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class VoyageController(http.Controller):

    @http.route('/voyage', type='http', auth='public', website=True)
    def voyage(self, **kw):
        depart_name = kw.get('depart')     # exemple: "Douala"
        arrivee_name = kw.get('arrivee')   # exemple: "Maroua"
        heure = kw.get('heure')            # exemple: "14:30"
        dispo = kw.get('dispo')            # exemple: "12"

        # Chercher les objets City correspondants
        departure_city = request.env['city'].sudo().search([('city_name', '=', depart_name)], limit=1)
        arrival_city = request.env['city'].sudo().search([('city_name', '=', arrivee_name)], limit=1)



        # Créer le voyage
        request.env['travel'].sudo().create({
            'departure_city': departure_city.id,
            'city_of_arrival': arrival_city.id,
            'heure_depart': heure,
            'nbre_place_disp': int(dispo)
        })

        return request.render('traffic.planning_template', {
            'depart': depart_name,
            'arrivee': arrivee_name,
            'heure': heure,
            'dispo': dispo
        })
