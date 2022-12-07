from odoo import models,fields,api

class DistrictDetails(models.Model):
    _name="district.details"
    _description="District Details"
    _rec_name = "district"

    district=fields.Char(string='District')