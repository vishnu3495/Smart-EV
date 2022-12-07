from odoo import models,api,fields,_
from odoo.exceptions import ValidationError


class VehicleDetails(models.Model):
    _name="cus_vehicle.details"
    _description="Vehicle Details"
    _rec_name = "reg_no"

    @api.model
    def get_user(self):
        customer = self.env['customer.details'].search([('user_id', '=', self.env.user.id)], limit=1)
        return customer and customer.id or False


    name_id = fields.Many2one('customer.details', string='Customer Name',required=True,default=get_user)
    vehicle_id=fields.Many2one('add_vehicle.details',string='Company Vehicle')
    model_id=fields.Many2one('cm_electric_vehicle.details',string='Company Model')
    image = fields.Binary(string="Customer Image")
    reg_no=fields.Char(string="Registration No:")
    date_reg=fields.Date(string="Date of Registration")
    chase_no=fields.Char(string="Chase No:")
    engine_no=fields.Char(string="Engine No:")
    fuel = fields.Char(string="Fuel",default='Battery')

    @api.onchange('vehicle_id')
    def onchange_cus_vehicle_id(self):
        domain = []
        for record in self:
            record.model_id = False
            if record.vehicle_id :
                domain.append(('id', 'in', record.vehicle_id.vehicle_ids.ids))
        return {'domain': {'model_id': domain}}

    @api.constrains('reg_no')
    def check_duplicate_reg_no(self):
        for rec in self:
            if len(self.search([('reg_no', '=', rec.reg_no)])) > 1:
                raise ValidationError('Registration Number %s Already Exist.!' % rec.reg_no)

    @api.model
    def create(self, values):
        if values.get('name_id', False):
            customer = self.env['customer.details'].browse(values.get('name_id'))
            if customer.state != 'approved':
                raise ValidationError('You are Not approved by admin...Please Contact the admin.!')
        return super(VehicleDetails, self).create(values)


