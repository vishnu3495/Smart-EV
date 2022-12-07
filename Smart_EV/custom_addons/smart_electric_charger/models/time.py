from odoo import models,fields,api

class ManagerDetails(models.Model):
    _name="time.details"
    _description="Time Details"
    _rec_name = "time"

    time=fields.Char(string="Time")

