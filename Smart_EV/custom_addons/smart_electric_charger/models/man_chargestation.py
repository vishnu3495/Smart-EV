from odoo import models,api,fields

class StationDetails(models.Model):
    _name="man_station.details"
    _description="Station Details"
    _rec_name = "com_name"


    refer=fields.Char(string='Reference')
    com_name=fields.Char(string="Company Name",required=True)
    district_id=fields.Many2one('district.details',string="District")
    place_id=fields.Many2one('place.details',string='Place')
    mobile=fields.Char(string='Mobile')
    email=fields.Char(string="Email")
    timing=fields.Selection([('24hr','24hr'),('12hr','12hr')],string='Timing')
    slot=fields.Integer(string="Slot Availability")
    reserved_slot=fields.Integer(string='Reserved Slot',compute='check_slot')
    power=fields.Char(string="Max Power O/P")
    avg_chg_time=fields.Char(string='Avg Charge Time')
    charger_type=fields.Char(string='Charger Type',default='AC/DC')
    image=fields.Binary(string="Image")
    booking_ids = fields.One2many('booking.details', 'com_name_id', string="Customer Details")

    @api.model
    def create(self, vals):
        vals['refer'] = self.env['ir.sequence'].next_by_code('man_station.details')
        return super(StationDetails, self).create(vals)

    # def write(self, vals):
    #     if not self.refer:
    #         vals['refer'] = self.env['ir.sequence'].next_by_code('man_station.details')
    #     return super(StationDetails, self).write(vals)

    @api.depends('booking_ids')
    def check_slot(self):
        for rec in self:
            reserved=0
            if rec.booking_ids:
                slot=len(rec.booking_ids.ids)
                reserved=slot
            rec.reserved_slot=reserved



