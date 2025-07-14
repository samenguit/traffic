from odoo import http
from odoo.http import request
from odoo.exceptions import AccessDenied

class TrafficLogin(http.Controller):

    # Affiche le formulaire
    @http.route('/login_resp', type='http', auth='public', website=True, methods=['GET'])
    def login_resp_form(self, **kw):
        return request.render('traffic.login_resp_template')

    # Traite le formulaire soumis
    @http.route('/login_resp_check', type='http', auth='public', website=True, methods=['POST'])
    def login_resp_check(self, **kw):
        username = kw.get('email')
        password = kw.get('password')

        try:
            uid = request.session.authenticate(request.env.cr.dbname, username, password)
        except AccessDenied:
            uid = None

        if uid:
            agency = request.env['agency'].sudo().search([('user_id', '=', uid)], limit=1)
            if agency:
                request.session['agency_id'] = agency.id
                return request.redirect('/espace_agence')
            else:
                return "Utilisateur trouvé, mais aucun client lié."
        else:
            return "Nom d'utilisateur ou mot de passe incorrect."
