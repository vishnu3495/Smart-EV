from odoo import models,fields,api

class ConnectorDetails(models.Model):
    _name="connector.details"
    _description="Connector Details"
    _rec_name = "con_type_id"

    type=fields.Selection([('ac','AC'),('dc','DC')],string="Connection Type")
    con_type_id=fields.Many2one('connect.details',string='Connector Type')
    typ_power=fields.Selection([('3.7KW','3.7KW'),('7KW','7KW'),('50KW','50KW'),('150KW','150KW')],string="Power Rating")
    approx_range=fields.Selection([('20KM','20KM'),('40KM','40KM'),('120KM','120KM'),('360KM','360KM')],string="Range for 30min")
    connector_id=fields.Many2one('add_vehicle.details')

