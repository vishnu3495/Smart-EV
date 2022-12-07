from odoo import models,fields,api

class PlaceDetails(models.Model):
    _name="place.details"
    _description="Place Details"
    _rec_name = "place"

    district_id=fields.Many2one('district.details',string='District')
    place=fields.Char(string='Place')