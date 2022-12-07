from odoo import api, fields, models,_


class ChargeStationWizard(models.TransientModel):
    _name = "charge_station.wizard"
    _description = "Charge Station Wizard"

    @api.model
    def default_get(self, fields):
        res = super(ChargeStationWizard, self).default_get(fields)
        browse_id = self.env['booking.details'].browse(self._context.get('active_id'))
        res.update({
            'cus_name_id': browse_id.cus_name_id.id,
            'image': browse_id.image,
            'reg_id': browse_id.reg_id.id,
            'vehicle_id': browse_id.vehicle_id.id,
            'model_id': browse_id.model_id.id,
            'com_name_id': browse_id.com_name_id.id,
            'date': browse_id.date,
            'times_id': browse_id.times_id.id,
            'type': browse_id.type,
            'con_type_id': browse_id.con_type_id.id,
            'booking_detail_id': browse_id.id
        })
        return res

    cus_name_id = fields.Many2one('customer.details', string="Customer Name", required=True)
    image = fields.Binary(string="Customer Image")
    reg_id = fields.Many2one('cus_vehicle.details', string="Registration No:")
    vehicle_id = fields.Many2one('add_vehicle.details', string='Company Vehicle')
    model_id = fields.Many2one('cm_electric_vehicle.details', string='Company Model')
    com_name_id = fields.Many2one('man_station.details', string="Station Name")
    date = fields.Date(string="Slot Date")
    times_id = fields.Many2one('time.details', string='Time')
    type = fields.Selection([('ac', 'AC'), ('dc', 'DC')], string="Connection Type")
    con_type_id = fields.Many2one('connect.details', string='Connector Type')
    booking_detail_id=fields.Many2one('booking.details')
    ini_chrg=fields.Char(string='Initial Charge(%)',required=True)
    ini_kilometer=fields.Char(string="Initial Range(km)",required=True)

    def action_charge(self):
        self.booking_detail_id.is_charge_completed=True
        charge_detail = self.env['charge.details']
        vals = {
            'cus_name_id': self.cus_name_id.id,
            'image':self.image,
            'reg_id': self.reg_id.id,
            'vehicle_id': self.vehicle_id.id,
            'model_id': self.model_id.id,
            'com_name_id': self.com_name_id.id,
            'date': self.date,
            'times_id': self.times_id.id,
            'type': self.type,
            'con_type_id': self.con_type_id.id,
            'booking_id':self.booking_detail_id.id,

            'ini_chrg': self.ini_chrg,
            'ini_kilometer': self.ini_kilometer

        }
        charge_obj = charge_detail.create(vals)
        return {
            'type': 'ir.actions.act_window',
            'name': 'smart_electric_charger.charge_form',
            'res_model': 'charge.details',
            'res_id': charge_obj.id,
            'view_mode': 'form',
            'target': 'current',
        }

