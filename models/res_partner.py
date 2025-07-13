from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'


    telegram_chat_id = fields.Char(string="Telegram Chat ID")
    cni = fields.Char('cni')
    username = fields.Char('username')
    password = fields.Char('password')




