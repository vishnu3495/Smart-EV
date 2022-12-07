from odoo import api, fields, models


class SearchStationWizard(models.TransientModel):
    _name = "search_station.wizard"
    _description = "Search Station Wizard"

    loc_id = fields.Many2one('district.details', string='District')
    place_id = fields.Many2one('place.details', string='Place')
    company_id = fields.Many2one('man_station.details', string='Company')

    def book_now_button(self):
        for rec in self:
            return {
                'res_model': 'booking.details',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_id': self.env.ref("smart_electric_charger.view_booking_form").id,
                'context':
                    {'default_dis_name_id': rec.loc_id.id, 'default_place_id': rec.place_id.id,'default_com_name_id':rec.company_id.id}

            }
