from odoo import models,api,fields

class BookingCustomer(models.Model):
    _name="booking_customer.details"
    _description="Booking Details"

    cust_name=fields.Char(string='Customer Name',required=True)
    date=fields.Date(string='Date')
    times_id=fields.Many2one('time.details',string='Time')
    book_detail_id=fields.Many2one('man_station.details')

