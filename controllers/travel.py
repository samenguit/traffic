from odoo import http
from odoo.http import request
import logging



_logger = logging.getLogger(__name__)
class TravelController(http.Controller):
    @http.route('/travel', type='http', auth='public', website=True)
    def travel_find(self, **kw):
        depart = kw.get('depart')
        arrivee = kw.get('arrivee')
        voyages = request.env['travel'].search([
            ('departure_city', 'ilike', depart),
            ('city_of_arrival', 'ilike', arrivee),
        ])
        types_disponibles = request.env['type_voyage'].search([])
        dates_disponibles = list(set(v.date_depart.strftime('%Y-%m-%d') for v in voyages))
        heures_disponibles = list(set(v.heure_depart for v in voyages))
        agence_disponibles = list(set(v.bus_id.agency_id.name for v in voyages if v.bus_id.agency_id.name))

        return request.render('traffic.travel_template', {
            'voyages': voyages,
            'depart': depart,
            'arrivee': arrivee,
            'types_disponibles': types_disponibles,
            'dates_disponibles': sorted(dates_disponibles),
            'heures_disponibles': sorted(heures_disponibles),
            'agence_disponibles': sorted(agence_disponibles),
        })

