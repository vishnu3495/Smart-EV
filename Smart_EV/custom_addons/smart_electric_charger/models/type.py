from odoo import models,fields,api

class CarTypeDetails(models.Model):
    _name="type.details"
    _description="Type Details"
    _rec_name = "type"

    type=fields.Char(string='Type')