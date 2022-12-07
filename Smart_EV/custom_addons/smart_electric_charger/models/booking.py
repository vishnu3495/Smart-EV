from odoo import models, fields, api


class BookingDetails(models.Model):
    _name = "booking.details"
    _description = "Booking Details"
    _rec_name = "cus_name_id"

    @api.model
    def get_user(self):
        customer = self.env['customer.details'].search([('user_id', '=', self.env.user.id)], limit=1)
        return customer and customer.id or False

    cus_name_id = fields.Many2one('customer.details', string="Customer Name", required=True,default=get_user)
    ref = fields.Char(string="Reference")
    age = fields.Integer(string="Age")
    gender = fields.Selection(
        [('male', 'Male'),
         ('female', 'Female'),
         ('other', 'Other')], string='Gender')
    address = fields.Text(string="Address")
    dob = fields.Date(string='Date of Birth')
    emails = fields.Char(string='Email')
    mobile = fields.Char(string='Mobile')
    image = fields.Binary(string="Customer Image")
    reg_id = fields.Many2one('cus_vehicle.details', string="Registration No:")
    vehicle_id = fields.Many2one('add_vehicle.details', string='Company Vehicle')
    model_id = fields.Many2one('cm_electric_vehicle.details', string='Company Model')
    vehicle = fields.Selection([
        ('bike', 'Bike'), ('car', 'Car')], string="Vehicle")
    date_reg = fields.Date(string="Date of Registration")
    chase_no = fields.Char(string="Chase No:")
    engine_no = fields.Char(string="Engine No:")
    fuel = fields.Char(string="Fuel", default='Battery')
    date = fields.Date(string="Slot Date")
    dis_name_id = fields.Many2one('district.details', string='District', required=True)
    place_id = fields.Many2one('place.details', string="Place")
    type = fields.Selection([('ac', 'AC'), ('dc', 'DC')], string="Connection Type")
    con_type_id=fields.Many2one('connect.details',string='Connector Type')
    times_id = fields.Many2one('time.details', string='Time')
    com_name_id = fields.Many2one('man_station.details', string="Station Name")
    state = fields.Selection([('draft', 'Draft'), ('booked', 'Booked'), ('cancelled', 'Cancelled')],
                             default='draft', string='Status')
    is_charge_completed = fields.Boolean(string='Charge Now')


    def action_draft(self):
        self.state = 'draft'

    def action_booked(self):
        self.state = 'booked'
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Booking Confirmed',
                'type': 'rainbow_man'
            }
        }

    def action_cancel(self):
        self.state = 'cancelled'

    @api.onchange('cus_name_id', 'reg_id')
    def onchange_cus_name_id(self):
        self.ref = self.cus_name_id and self.cus_name_id.ref or ''
        self.age = self.cus_name_id and self.cus_name_id.age or ''
        self.gender = self.cus_name_id and self.cus_name_id.gender or ''
        self.address = self.cus_name_id and self.cus_name_id.address or ''
        self.dob = self.cus_name_id and self.cus_name_id.dob or ''
        self.emails = self.cus_name_id and self.cus_name_id.emails or ''
        self.mobile = self.cus_name_id and self.cus_name_id.mobile or ''
        self.image = self.cus_name_id and self.cus_name_id.image or ''
        self.vehicle_id = self.reg_id and self.reg_id.vehicle_id or ''
        self.model_id = self.reg_id and self.reg_id.model_id or ''
        self.date_reg = self.reg_id and self.reg_id.date_reg or ''
        self.chase_no = self.reg_id and self.reg_id.chase_no or ''
        self.engine_no = self.reg_id and self.reg_id.engine_no or ''
        self.fuel = self.reg_id and self.reg_id.fuel or ''

    @api.onchange('vehicle_id','type')
    def onchange_connector(self):
        connector=[]
        for rec in self:
            company=self.env['add_vehicle.details'].browse(rec.vehicle_id.id)
            if company:
                for line in company.connector_ids:
                    if line.type==rec.type:
                        connector.append(line.con_type_id.id)
        return {'domain': {'con_type_id': [('id', 'in',list(set(connector)))]}}
