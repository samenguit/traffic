from odoo import models

class AccountMove(models.Model):
    _inherit = 'account.move'

    def _post(self, soft=True):
        res = super()._post(soft)
        for move in self:
            if move.move_type == 'out_invoice' and move.payment_state == 'paid':
                move._notify_traffic_driver_payment()
        return res

    def _notify_traffic_driver_payment(self):
        reservation = self.env['traffic.reservation'].search([('invoice_id', '=', self.id)], limit=1)
        if reservation and reservation.travel_id.driver_id.telegram_chat_id:
            chauffeur = reservation.travel_id.driver_id
            message = (
                f"Bonjour {chauffeur.name},\n"
                f"Un paiement a été reçu pour le voyage de {reservation.customer_id.name} "
                f"de {reservation.travel_id.departure_city.name} à {reservation.travel_id.arrival_city.name}.\n"
                f"Heure de départ : {reservation.travel_id.departure_time}"
            )
            self.env['telegram.bot'].send_message_to_chat(
                chat_id=chauffeur.telegram_chat_id,
                message=message
            )
