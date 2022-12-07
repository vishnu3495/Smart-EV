from odoo import models

class PatientCardXlsx(models.AbstractModel):
    _name = 'report.smart_electric_charger.report_company_details_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, customers):
        sheet = workbook.add_worksheet('Appointment Record')
        format = workbook.add_format({'bold': True, 'font_color': 'black', 'align': 'center', 'border':7})
        format_1 = workbook.add_format({'font_color': 'black', 'align': 'left'})
        format_2 = workbook.add_format({'bold': True, 'font_color': '#6f4e37', 'align': 'center'})
        format_3 = workbook.add_format({'font_color': 'black', 'align': 'right'})
        date=workbook.add_format({'font_color':'black','num_format':'dd-mm-yyyy','align':'right'})

        wiz_model=data['context'].get('active_model',False)
        if not wiz_model:
            wiz_model='appointment.report.wizard'
        wiz_id=self.env[wiz_model].browse(data['context'].get('active_id',False))
        if wiz_id:
            customer_data=wiz_id.get_appointment_report_wizard()
            if customer_data:

                sheet.set_column('A:B', 8)
                sheet.set_column('C:D', 8)
                sheet.set_column('E:F', 8)
                sheet.set_column('G:H', 8)
                sheet.set_column('I:J', 8)

                sheet.merge_range('A1:J1', 'CUSTOMER DETAILS', format_2)
                row = 1
                col = 0

                sheet.merge_range(row, col, row, col + 1, 'CUSTOMER NAME', format)
                col = col + 2
                sheet.merge_range(row, col, row, col + 1, 'VEHICLE', format)
                col = col + 2
                sheet.merge_range(row, col, row, col + 1, 'MODEL', format)
                col = col + 2
                sheet.merge_range(row, col, row, col + 1, 'DATE', format)
                col = col + 2
                sheet.merge_range(row, col, row, col + 1, 'TIME', format)

                for obj in customer_data:

                    row = row + 1
                    col = 0
                    sheet.merge_range(row, col, row, col + 1, obj.cus_name_id.cus_name, format_1)
                    col += 2
                    sheet.merge_range(row, col, row, col + 1, obj.vehicle_id.company_id.company, format_1)
                    col += 2
                    sheet.merge_range(row, col, row, col + 1, obj.model_id.com_model, format_3)
                    col+=2
                    sheet.merge_range(row, col, row, col + 1, obj.date, date)
                    col += 2
                    sheet.merge_range(row, col, row, col + 1, obj.times_id.time, format_3)







