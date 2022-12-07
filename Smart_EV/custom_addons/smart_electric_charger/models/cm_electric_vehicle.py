from odoo import models,api,fields

class CompanyElectric(models.Model):
    _name="cm_electric_vehicle.details"
    _description="Electric Vehicle Details"
    _rec_name = "com_model"

    refs=fields.Char(string='Reference')
    img = fields.Binary(string="Vehicle")
    com_model = fields.Char(string='Model')
    type_id=fields.Many2one('type.details',string="Car Type")
    range=fields.Char(string="Range")
    max_torque=fields.Char(string="Max Torque(nm@rpm)")
    body_type=fields.Char(string="Body Type")
    max_power=fields.Char(string="Max Power(bhp@rpm")
    boot_space=fields.Char(string="Boot Space(Litres)")
    battery=fields.Char(string="Battery Capacity")
    ground_clearance=fields.Char(string="Ground Clearance Unladen")

    com_model_id = fields.Many2one('add_vehicle.details', string="Model")

    @api.model
    def create(self, vals):
        vals['refs'] = self.env['ir.sequence'].next_by_code('cm_electric_vehicle.details')
        return super(CompanyElectric, self).create(vals)

    # def write(self, vals):
    #     if not self.refs:
    #         vals['refs'] = self.env['ir.sequence'].next_by_code('cm_electric_vehicle.details')
    #     return super(CompanyElectric, self).write(vals)
