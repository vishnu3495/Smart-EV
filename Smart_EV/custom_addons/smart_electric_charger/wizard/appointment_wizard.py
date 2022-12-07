from odoo import api,fields,models,_

class AppointmentReportWizard(models.TransientModel):
    _name="appointment.report.wizard"
    _description="Print Appointment Wizard"

    com_name_id = fields.Many2one('man_station.details', string="Station Name")
    date_from=fields.Date(string='Date From')
    date_to=fields.Date(string="Date To")

    def get_appointment_report_wizard(self):
        domain=[]
        com_name_id=self.com_name_id
        if com_name_id:
            domain.append(('com_name_id','=',com_name_id.id))
        date_from=self.date_from
        if date_from:
            domain.append(('date','>=',date_from))
        date_to=self.date_to
        if date_to:
            domain.append(('date','<=',date_to))
        appointments=self.env['booking.details'].search(domain)
        return appointments

    def generate_xlsx(self):
        for rec in self:
            data={
                'ids':rec.ids,
                'model':rec._name,
                'form':{}
            }
            return self.env.ref('smart_electric_charger.report_company_appointment_xlsx').report_action(self, data=data)


