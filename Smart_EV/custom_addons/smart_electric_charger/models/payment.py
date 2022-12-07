from odoo import models,fields,api

class PaymentDetails(models.Model):
    _name="payment.details"
    _description="Payment Details"
    _rec_name = "card_name"


    card=fields.Selection([('credit','Credit'),
         ('debit','Debit')],string='Credit/Debit')
    card_name=fields.Char(string='Card Holder Name')
    card_no=fields.Char(string='Card Number')
    exp_date=fields.Char(string="Expiry Date (MM/YY)")
    cvv=fields.Integer(string='CVV')
    booking_id=fields.Many2one('booking.details')
    card_id=fields.Many2one('charge.details')
    user_id = fields.Many2one('res.users')
    state = fields.Selection([('draft','Draft'),('pay', 'Waiting for approval'),('approved','Paid'),],string='Status',default='draft')

    def action_pay(self):
        self.state='pay'

    def action_approved(self):
        self.state = 'approved'
        self.card_id.action_email()
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Payment Completed Successfully',
                'type': 'rainbow_man'
            }
        }

    def generate_pdf(self):
        return self.card_id.generate_pdf_report()



