from odoo import http
from odoo.http import request
import logging



_logger = logging.getLogger(__name__)
class RegistrationController(http.Controller):


    @http.route('/registration', type='http', auth="public", website=True)
    def inscription(self):
        return request.render('traffic.registration_template')



    @http.route('/inscription_client', type='http', auth='public', website=True, methods=['GET', 'POST'])
    def inscription_client(self, **post):
        if http.request.httprequest.method == 'POST':
            email = post.get('email')
            username = post.get('username')
            password = post.get('password')
            phone = post.get('phone')

            # Vérifier si l'email existe déjà
            existing = request.env['res.users'].sudo().search([('login', '=', email)], limit=1)
            if existing:
                return request.render('traffic.erreur_template', {'message': "Email déjà utilisé."})

            # Créer utilisateur dans res.users
            user = request.env['res.users'].sudo().create({
                'name': username,
                'login': email,
                'email': email,
                'password': password,
                'active': True,
                'groups_id': [(6, 0, [
                    request.env.ref('base.group_user').id,
                    # tu peux ajouter d'autres groupes ici si besoin
                ])]
            })

            # Créer customer personnalisé
            request.env['customer'].sudo().create({
                'user_id': user.id,
                'email': email,
                'username': username,
                'phone': phone
            })

            # Rediriger vers l’espace personnel
            return request.redirect('/mon_espace')


        return request.render('ton_module.inscription_client_template')
