import requests
from odoo import models

class TelegramBot(models.AbstractModel):
    _name = 'telegram.bot'
    _description = 'Bot pour envoi de message Telegram'

    def send_message_to_chat(self, chat_id, message):
        token = '7915085167:AAFWGbOk2w4HRF2IIowp5SGeTOCr0UrpGqo'
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {'chat_id': chat_id, 'text': message}
        response = requests.post(url, data=data)
        return response.json()
