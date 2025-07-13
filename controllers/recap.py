from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class RecapController(http.Controller):
    @http.route('/recap/<int:voyage_id>', type='http', auth='public', website=True, methods=['POST'])
    def travel_facturation(self, voyage_id, **kw):
        nom = kw.get('nom')
        phone = kw.get('phone')
        cni = kw.get('cni')
        reservation = request.env['booking'].sudo().create({
            'name': nom,
            'cni_number': cni,
            'phone': phone,
            'travel_id': voyage_id,
        })
        return request.render("traffic.recap_template", {
            'voyage': reservation,
        })