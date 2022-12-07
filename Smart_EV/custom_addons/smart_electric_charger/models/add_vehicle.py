from odoo import models,api,fields
from odoo.exceptions import ValidationError

class AddVehicle(models.Model):
    _name="add_vehicle.details"
    _description="Add Company"
    _rec_name = "company_id"

    @api.model
    def get_user(self):
        manager = self.env['manager.details'].search([('user_id', '=', self.env.user.id)], limit=1)
        return manager and manager.id or False

    names_id = fields.Many2one('manager.details', string='Manager Name', required=True, default=get_user)
    company_id = fields.Many2one('company.details',string='Company Name',required=True)
    image = fields.Binary(string="Station Image")
    vehicle_ids = fields.One2many('cm_electric_vehicle.details','com_model_id',string="Vehicle Details")
    connector_ids = fields.One2many('connector.details','connector_id',string='Connector Details')

    @api.constrains('company_id')
    def check_company(self):
        for rec in self:
            if rec.company_id:
                company=self.search([('company_id', '=', rec.company_id.id)])
                if company and len(company.ids) >1:
                    raise ValidationError('Company %s is already created.!' % rec.company_id.company)

    @api.model
    def create(self, values):
        if values.get('names_id', False):
            manager = self.env['manager.details'].browse(values.get('names_id'))
            if manager.state != 'approved':
                raise ValidationError('You are Not approved by admin...Please Contact the admin.!')
        return super(AddVehicle, self).create(values)





