from odoo import http
from odoo.http import request
from odoo.exceptions import AccessDenied

class TrafficLogin(http.Controller):

    @http.route('/login', type='http', auth='public', website=True, methods=['POST'])
    def connexion(self, **kw):
        return request.render('traffic.loggin_template')

    @http.route('/loggin_check', type='http', auth='public', website=True, methods=['POST'])
    def connexion_check(self, **kw):
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
                return request.redirect('/mon_espace')
            else:
                return "Utilisateur trouvé, mais aucun client lié."
        else:
            return "Nom d'utilisateur ou mot de passe incorrect."
