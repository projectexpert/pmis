# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import fields, orm


class AnalyticWipReport(orm.TransientModel):
    _name = 'analytic.wip.report'
    _description = 'Work In Progress Statement Report'

    _columns = {
        'from_date': fields.date('From'),
        'to_date': fields.date('To'),
    }

    def analytic_wip_report_open_window(self, cr, uid, ids, context=None):
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        result_context = {}
        if context is None:
            context = {}
        result = mod_obj.get_object_reference(
                cr, uid, 'analytic_wip_report',
                'action_account_analytic_account_wip_form')
        id = result and result[1] or False
        result = act_obj.read(cr, uid, [id], context=context)[0]
        data = self.read(cr, uid, ids, [])[0]
        if data['from_date']:
            result_context.update({'from_date': data['from_date']})
        if data['to_date']:
            result_context.update({'to_date': data['to_date']})
        result['context'] = str(result_context)
        return result
