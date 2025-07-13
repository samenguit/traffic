from odoo import http
from odoo.http import request
import base64

class DriverController(http.Controller):

    @http.route('/driver', type='http', auth='public', website=True)
    def driver_registration(self):
        return request.render('traffic.registration_driver_template')

    @http.route('/driver/upload_documents_submit', type='http', auth='user', methods=['POST'], website=True)
    def upload_documents_submit(self, **post):
        user = request.env.user
        phone = post.get('phone')
        name = post.get('name')
        driver = request.env['driver'].sudo().create({
            'phone': phone,
            'name' : name
        })

        # Fichiers transmis dans le formulaire
        permis_file = post.get('permis')
        if permis_file:
            permis_data = permis_file.read()
            driver.sudo().write({
                'permis_scan': base64.b64encode(permis_data),
                'permis_filename': permis_file.filename,
            })

        cni_file = post.get('cni')
        if cni_file:
            cni_data = cni_file.read()
            driver.sudo().write({
                'cni_scan': cni_file.read(),
                'cni_filename': cni_file.filename,
            })

        assurance_file = post.get('assurance')
        if assurance_file:
            driver.sudo().write({
                'assurance_scan': assurance_file.read(),
                'assurance_filename': assurance_file.filename,
            })

        carte_grise_file = post.get('carte_grise')
        if carte_grise_file:
            driver.sudo().write({
                'carte_grise_scan': carte_grise_file.read(),
                'carte_grise_filename': carte_grise_file.filename,
            })

        return request.render("traffic.registration_driver_template")  # si tu veux une page de confirmation propre
