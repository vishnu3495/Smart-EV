from odoo import models,fields,api,_
from datetime import datetime

try:
   import qrcode
except ImportError:
   qrcode = None
try:
   import base64
except ImportError:
   base64 = None
from io import BytesIO


class ChargeDetails(models.Model):
    _name="charge.details"
    _description="Charging Details"
    _rec_name = "cus_name_id"

    cus_name_id = fields.Many2one('customer.details', string="Customer Name",required=True)
    image = fields.Binary(string="Customer Image")
    reg_id = fields.Many2one('cus_vehicle.details', string="Registration No:")
    vehicle_id = fields.Many2one('add_vehicle.details', string='Company Vehicle')
    model_id = fields.Many2one('cm_electric_vehicle.details', string='Company Model')
    com_name_id = fields.Many2one('man_station.details', string="Station Name")
    date = fields.Date(string="Slot Date")
    times_id = fields.Many2one('time.details', string='Time')
    type = fields.Selection([('ac', 'AC'), ('dc', 'DC')], string="Connection Type")
    con_type_id = fields.Many2one('connect.details', string='Connector Type')
    ini_kilometer = fields.Integer(string="Initial Range(Km)")
    ini_chrg=fields.Integer(string='Initial(%)')
    fin_chrg = fields.Integer(string='Final Charge(%)',compute= '_get_hours')
    fin_kilometer = fields.Integer(string="Final Range(Km)",compute='_get_hours')
    ser_charge=fields.Integer(string='Service Charge',compute= '_get_hours')
    sub_total=fields.Integer(string="Sub Total",compute= '_get_hours')
    amount=fields.Integer(string='Amount',compute= '_get_hours')
    start_time = fields.Datetime(string='Start Time')
    stop_time = fields.Datetime(string='Stop Time')
    hours_time=fields.Float(string='Working Hours',compute= '_get_hours')
    state = fields.Selection([('draft','Draft'),('charge', 'Charging'), ('stop', 'Stopped')],
                              default='draft',string='Status')
    booking_id=fields.Many2one('booking.details')
    is_payment_created=fields.Boolean(string='Payment')

    def action_charge(self):
        for rec in self:
            rec.start_time = fields.datetime.now()
            rec.state = 'charge'
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Charging Started',
                    'type': 'rainbow_man'
                }
            }

    def action_stop(self):
        for rec in self:
            rec.stop_time = fields.datetime.now()
            rec.state = 'stop'
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Charging Stopped',
                    'type': 'rainbow_man'
                }
            }

    @api.depends('start_time','stop_time','ini_kilometer','ini_chrg')
    def _get_hours(self):
        ser_charge = 30
        full_charge=100
        for rec in self:
            if rec.start_time and rec.stop_time:
                check_in_out_diff = rec.stop_time - rec.start_time
                if check_in_out_diff:
                    duration_sec = check_in_out_diff.total_seconds()
                    duration_hours = duration_sec / 3600
                    rec.hours_time = duration_hours

                    rec.amount=duration_hours*300
                    rec.ser_charge=ser_charge
                    rec.sub_total=rec.amount+rec.ser_charge

                    final_km = rec.hours_time * 200 + rec.ini_kilometer
                    rec.fin_kilometer = final_km

                    value=(duration_hours*full_charge)-rec.ini_chrg
                    if value<0:
                        rec.fin_chrg=value*(-1)
                    else:
                        rec.fin_chrg=value
            else:
                rec.hours_time=0
                rec.amount=0
                rec.ser_charge=0
                rec.sub_total=0
                rec.fin_kilometer=0
                rec.fin_chrg=0

    def generate_pdf_report(self):
        return self.env.ref('smart_electric_charger.actions_payment_card_id').report_action(self)

    def action_email(self):
        template_id = self.env.ref('smart_electric_charger.smart_electric_charger_payment_email').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    def get_bill_qrcode(self, qr_value):
        to_qr = qr_value or '*****'
        name = False
        qrcode_img = False
        if to_qr:
            info = qr_value
            name = "%s.png" % (qr_value)
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=20, border=4)
            qr.add_data(info)
            qr.make(fit=True)
            img = qr.make_image()
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            qrcode_img = base64.b64encode(buffer.getvalue())
        return qrcode_img
