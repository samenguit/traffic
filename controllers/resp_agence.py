from odoo import http
from odoo.http import request
import logging

from odoo.exceptions import AccessDenied


_logger = logging.getLogger(__name__)


class Respagence(http.Controller):
    @http.route('/resp_agence', type='http', auth='public', website=True)
    def connexion_agence(self, **kw):
        return request.render('traffic.loggin_agence_template')

    @http.route('/loggin_agence_check', type='http', auth='public', website=True, methods=['POST'])
    def connexion_agence_check(self, **kw):
        username = kw.get('email')
        password = kw.get('password')

        # Essayer d'authentifier via res.users
        try:
            uid = request.session.authenticate(request.env.cr.dbname, username, password)
        except AccessDenied:
            uid = None

        if uid:
            # Trouver le customer lié à ce user
            customer = request.env['customer'].sudo().search([('user_id', '=', uid)], limit=1)
            if customer:
                request.session['customer_id'] = customer.id
                return request.redirect('/espace_agence')
            else:
                return "Utilisateur trouvé, mais aucun client lié."
        else:
            return "Nom d'utilisateur ou mot de passe incorrect."
