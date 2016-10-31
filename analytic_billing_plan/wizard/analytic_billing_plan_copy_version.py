# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#              <contact@eficent.com>
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

from openerp.osv import fields, osv
from openerp.tools.translate import _


class AnalyticBillingPlanCopyVersion(osv.osv_memory):
    """
    For copying all the planned billings to a separate planning version
    """
    _name = "analytic.billing.plan.copy.version"
    _description = "Analytic Billing Plan copy versions"

    _columns = {
        'source_version_id': fields.many2one('account.analytic.plan.version',
                                             'Source Planning Version',
                                             required=True),
        'dest_version_id': fields.many2one('account.analytic.plan.version',
                                           'Destination Planning Version',
                                           required=True),
        'include_child': fields.boolean('Include child accounts'),
    }

    _defaults = {
        'include_child': True,
    }

    def analytic_billing_plan_copy_version_open_window(
            self, cr, uid, ids, context=None):

        if context is None:
            context = {}
        new_line_plan_ids = []
        analytic_obj = self.pool.get('account.analytic.account')
        line_plan_obj = self.pool.get('analytic.billing.plan.line')
        plan_version_obj = self.pool.get('account.analytic.plan.version')

        data = self.read(cr, uid, ids, [], context=context)[0]
        record_ids = context and context.get('active_ids', False)
        include_child = data.get('include_child', False)
        source_version_id = data.get('source_version_id', False)
        dest_version_id = data.get('dest_version_id', False)
        dest_version = plan_version_obj.browse(cr, uid,
                                               dest_version_id[0],
                                               context=context)
        if dest_version.default_plan:
            raise osv.except_osv(_('Error !'),
                                 _('It is prohibited to copy '
                                   'to the default planning version.'))

        if source_version_id == dest_version_id:
            raise osv.except_osv(_('Error !'),
                                 _('Choose different source and destination '
                                   'planning versions.'))
        if include_child:
            account_ids = analytic_obj.get_child_accounts(
                cr, uid, record_ids, context=context).keys()
        else:
            account_ids = record_ids

        line_plan_ids = line_plan_obj.search(
            cr, uid, [('account_id', 'in', account_ids),
                      ('version_id', '=', source_version_id[0])],
            context=context)

        for line_plan_id in line_plan_ids:
            new_line_plan_id = line_plan_obj.copy(
                cr, uid, line_plan_id, context=context
            )
            new_line_plan_ids.append(new_line_plan_id)

        line_plan_obj.write(
            cr, uid, new_line_plan_ids,
            {'version_id': dest_version_id[0]}, context=context
        )

        return {
            'domain': "[('id','in', ["+','.join(
                map(
                    str, new_line_plan_ids
                )
            )+"])]",
            'name': _('Billing Plan Lines'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'analytic.billing.plan.line',
            'view_id': False,
            'context': False,
            'type': 'ir.actions.act_window'
        }
