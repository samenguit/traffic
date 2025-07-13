from odoo import models, fields

class City(models.Model):
    _name = 'city'
    _description = 'city name'
    _rec_name = 'city_name'



    city_name = fields.Char('city name')




