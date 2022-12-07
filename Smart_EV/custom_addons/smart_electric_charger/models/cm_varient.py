from odoo import models,fields,api

class Connector(models.Model):
    _name="connect.details"
    _description="Connector Details"
    _rec_name = "name"

    name=fields.Char(string="Connector")


