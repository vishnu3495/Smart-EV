from odoo import models,fields,api

class CompanyDetails(models.Model):
    _name="company.details"
    _description="Company Details"
    _rec_name = "company"

    company=fields.Char(string='Company')

