from odoo import models,fields,api,_
from datetime import date
from odoo.exceptions import ValidationError



class CustomerDetails(models.Model):
    _name="customer.details"
    _description="Customer Details"
    _rec_name = "cus_name"

    ref=fields.Char(string="Reference")
    cus_name=fields.Char(string="Name",required=True)
    age = fields.Integer(compute="compute_get_age",string="Age")
    gender=fields.Selection(
        [('male','Male'),
         ('female','Female'),
         ('other','Other')],string='Gender')
    address=fields.Text(string="Address")
    dob=fields.Date(string='Date of Birth')
    emails=fields.Char(string='Email')
    mobile=fields.Char(string='Mobile')
    image=fields.Binary(string="Customer Image")
    status=fields.Char(string='Status')
    user_id=fields.Many2one('res.users')
    email_to=fields.Char(string='Email To',default='vishnurajendran3495@gmail.com')
    state = fields.Selection([('draft', 'Draft'), ('approved', 'Approved'), ('cancelled', 'Cancelled')], default='draft',
                             string='Status')

    def action_draft(self):
        self.state = 'draft'

    def action_approve(self):
        self.state = 'approved'

    def action_cancel(self):
        self.state = 'cancelled'

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('customer.details')
        return super(CustomerDetails, self).create(vals)

    def write(self, vals):
        if not self.ref:
            vals['ref'] = self.env['ir.sequence'].next_by_code('customer.details')
        return super(CustomerDetails, self).write(vals)

    @api.depends('dob')
    def compute_get_age(self):
        today_date = date.today()
        for rec in self:
            age = 0
            if rec.dob:
                db = rec.dob
                age = int((today_date - db).days / 365)
            rec.age = age

    @api.constrains('emails')
    def check_emails(self):
        for rec in self:
            if rec.emails:
                getemails=self.search([('emails', '=', rec.emails)])
                if getemails and len(getemails.ids)>1:
                    raise ValidationError('Email %s already existed!' % rec.emails)

    @api.constrains('dob')
    def check_dob(self):
        today_date = date.today()
        for rec in self:
            if rec.dob and rec.dob >= today_date:
                raise ValidationError('Enter a valid Date of Birth')


    def unlink(self):
        if self.state == 'approved':
            raise ValidationError(_("You Cannot Delete %s because he/she in approved state" % self.cus_name))
        return super(CustomerDetails, self).unlink()







