from odoo import http
from odoo.http import request
import logging



_logger = logging.getLogger(__name__)


class SearchController(http.Controller):
    @http.route('/search', type='http', auth='public',website=True)
    def travel_recherche(self, **kw):
        return request.render('traffic.search_template')