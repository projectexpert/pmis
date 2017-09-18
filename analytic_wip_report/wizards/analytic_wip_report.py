# -*- coding: utf-8 -*-
# Copyright 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AnalyticWipReport(models.TransientModel):
    _name = 'analytic.wip.report'
    _description = 'Work In Progress Statement Report'

    from_date = fields.Date('From')
    to_date = fields.Date('To')

    @api.multi
    def analytic_wip_report_open_window(self):
        mod_obj = self.env['ir.model.data']
        act_obj = self.env['ir.actions.act_window']
        result_context = {}
        result = mod_obj.\
            get_object_reference('analytic_wip_report',
                                 'action_account_analytic_account_wip_form')
        id = result and result[1] or False
        result = act_obj.search([('id', '=', id)])
        result = result.read()[0]
        data = self.read()[0]
        if data['from_date']:
            result_context.update({'from_date': data['from_date']})
        if data['to_date']:
            result_context.update({'to_date': data['to_date']})
        result['context'] = str(result_context)
        return result
