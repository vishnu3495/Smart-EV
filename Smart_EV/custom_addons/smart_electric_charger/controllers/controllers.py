# -*- coding: utf-8 -*-
from odoo import http, api
from odoo.http import request


class RegisterSystem(http.Controller):
    @http.route('/register_webform', type="http", auth='public', website=True)
    def reg_form(self):
        return http.request.render('smart_electric_charger.reg_details')

    @http.route('/register/details', type="http", auth='public', website=True)
    def form_submit(self, **kwargs):
        group_id=False
        if kwargs.get('user') == 'customer':
            data = request.env['customer.details'].sudo().create({
                'cus_name': kwargs.get('cus_name'),
                'gender': kwargs.get('gender'),
                'address': kwargs.get('address'),
                'dob': kwargs.get('dob'),
                'emails': kwargs.get('emails'),
                'mobile': kwargs.get('mobile'),
            })

            group_id = request.env.ref('smart_electric_charger.group_smart_ev_customer').id
        else:
            data = request.env['manager.details'].sudo().create({
                'man_name': kwargs.get('cus_name'),
                'gender': kwargs.get('gender'),
                'address': kwargs.get('address'),
                'dob': kwargs.get('dob'),
                'email': kwargs.get('emails'),
                'mobile': kwargs.get('mobile'),
            })
            group_id = request.env.ref('smart_electric_charger.group_smart_ev_manager').id
        vals = {
            'register_system': data,
        }

        user_id = request.env['res.users'].sudo().create({
            'name': kwargs.get('cus_name'),
            'login': kwargs.get('emails'),

        })
        data.user_id = user_id.id


        if user_id and group_id:
            group = request.env['res.groups'].sudo().browse(group_id)
            if user_id not in group.users.ids:
                group.sudo().write({'users': [(4, user_id.id)]})

        if user_id:
            change_password_wiz = request.env['change.password.wizard'].with_context(active_id=user_id.id,
                                                                                     active_ids=[user_id.id],
                                                                                     active_model='res.users').sudo().create({})
            for line in change_password_wiz.user_ids:
                line.sudo().new_passwd = kwargs.get('password')
            change_password_wiz.sudo().change_password_button()
        return request.render("smart_electric_charger.register_form_success", vals)
