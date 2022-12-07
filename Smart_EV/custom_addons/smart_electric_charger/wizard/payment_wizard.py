from odoo import api, fields, models,_


class PaymentWizard(models.TransientModel):
    _name = "payment.wizard"
    _description = "Payment Wizard"

    @api.model
    def default_get(self, fields):
        res = super(PaymentWizard, self).default_get(fields)
        browse_id = self.env['charge.details'].browse(self._context.get('active_id'))
        res.update({
            'card_id': browse_id and browse_id.id or False})
        return res

    card_id = fields.Many2one('charge.details')

    def pay_now_button(self):
        for rec in self:
            payment = self.env['payment.details'].create({'card_id': rec.card_id.id,'booking_id':rec.card_id.booking_id.id})
            rec.card_id.is_payment_created=True
            form_view_id = self.env.ref('smart_electric_charger.payment_form').id
            return {
                'name': _('Payment'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'payment.details',
                'views': [(form_view_id, 'form')],
                'view_id': form_view_id,
                'target': 'current',
                'res_id': payment.id,
                'context': {'form_view_initial_mode': 'edit', 'force_detailed_view': 'true'}
            }

