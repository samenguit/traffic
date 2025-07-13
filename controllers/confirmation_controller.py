from odoo import http
from odoo.http import request
import logging
from odoo.exceptions import UserError






_logger = logging.getLogger(__name__)
class ConfirmationController(http.Controller):
    @http.route('/confirmation/<int:voyage_id>/<string:cni>', type='http', auth='user', website=True)
    def confirmation(self, voyage_id,cni):
        travel = request.env['travel'].sudo().browse(voyage_id)
        chat_id = travel.driver_id.telegram_chat_id

        # Rechercher la réservation spécifique par nom
        booking = request.env['booking'].sudo().search([
            ('travel_id', '=', travel.id),
            ('cni_number', '=', cni)
        ], limit=1)

        if not booking:
            return f"Aucune réservation trouvée pour."

            # Sécurité : vérifier le chat_id
        chat_id = 5656595176
        if not chat_id:

            raise UserError("Ce chauffeur n'a pas de chat_id Telegram.")

        # Message de confirmation
        driver_name = travel.driver_name or "Chauffeur inconnu"
        partner_name = booking.name or "Client inconnu"
        place_reserv = booking.nbre_place_reserv
        message = f"Bonjour {driver_name}, vous venez de recevoir le paiement de la reservation de {place_reserv} place de  {partner_name}."

        # Envoi Telegram
        request.env['telegram.bot'].send_message_to_chat(
            chat_id=chat_id,
            message=message
        )

        request.env['res.partner'].sudo().create({
            'name' : booking.name,
            'cni': booking.cni_number,
            'phone': booking.phone,
        })


        #mise a jour des places

        travel.nbre_place_disp = travel.nbre_place_disp - booking.nbre_place_reserv


        #email client
        IrModelData = request.env['ir.model.data'].sudo()
        MailTemplate = request.env['mail.template'].sudo()

        # 1. Vérifie si le template existe déjà (via xml_id)
        try:
            template = request.env.ref('traffic.mail_template_booking_confirmation')

        except ValueError:
            template = None

        # 2. S’il n’existe pas, on le crée et on l’enregistre
        if not template:
            model_id = request.env['ir.model'].sudo().search([('model', '=', 'booking')], limit=1).id
            template = MailTemplate.create({
                'name': 'Confirmation Réservation',
                'model_id': model_id,
                'subject': 'Confirmation de votre réservation',
                'body_html': """
                    <p>Bonjour ${object.name},</p>
                    <p>Votre réservation pour le voyage <strong>${object.travel_id}</strong> est confirmée.</p>
                    <p>Nombre de places réservées : ${object.nbre_place_reserv}</p>
                    <p>Montant total : ${object.amount_total} FCFA</p>
                    <p>Merci pour votre confiance.</p>
                """,
                'email_from': 'arthursamenguit@gmail.com',
                'email_to': '${object.email}',
            })

            # 3. Enregistrer le template comme une référence technique pour le retrouver plus tard
            IrModelData.create({
                'name': 'mail_template_booking_confirmation',
                'model': 'mail.template',
                'module': 'traffic',
                'res_id': template.id,
                'noupdate': True,
            })

        # 4. Envoi du mail
        template.send_mail(booking.id, force_send=True)



        # Rendu de la facture ou confirmation
        return request.render('traffic.invoicing_template', {
            'booking': booking,
            'voyage': travel,
        })



