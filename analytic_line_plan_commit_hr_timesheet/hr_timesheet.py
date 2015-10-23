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

from openerp.osv import fields
from openerp.osv import osv
from openerp.tools.translate import _


class hr_employee(osv.osv):
    _name = "hr.employee"
    _inherit = "hr.employee"
    _columns = {
        'plan_journal_id': fields.many2one(
            'account.analytic.plan.journal',
            'Planning Analytic Journal'
        ),
    }

hr_employee()


class hr_analytic_timesheet(osv.osv):

    _inherit = "hr.analytic.timesheet"

    _columns = {
        'analytic_line_plan': fields.many2one(
            'account.analytic.line.plan', 'Planning Analytic line'
        ),
    }

    def _getAnalyticPlanJournal(self, cr, uid, context=None):
        emp_obj = self.pool.get('hr.employee')
        if context is None:
            context = {}
        emp_id = emp_obj.search(
            cr, uid,
            [('user_id', '=', context.get('user_id', uid))],
            context=context
        )
        if emp_id:
            emp = emp_obj.browse(cr, uid, emp_id[0], context=context)
            if emp.plan_journal_id:
                return emp.plan_journal_id.id
        return False

    def create(self, cr, uid, vals, *args, **kwargs):
        line_plan_obj = self.pool.get('account.analytic.line.plan')
        plan_version_obj = self.pool.get('account.analytic.plan.version')
        vals_line = {}
        context = kwargs.get('context', {})

        version_id = plan_version_obj.search(
            cr, uid, [('default_committed', '=', True)], context=context
        )[0]
        if not version_id:
            raise osv.except_osv(
                _('Error!'),
                _(
                    'Please define an analytic planning version '
                    'as default for committed costs.'
                )
            )
        vals_line['name'] = vals['name']
        vals_line['date'] = vals['date']
        vals_line['amount'] = vals['amount']
        vals_line['amount_currency'] = vals['amount']
        vals_line['unit_amount'] = vals['unit_amount']
        vals_line['account_id'] = vals['account_id']
        vals_line['company_id'] = self.pool.get(
            'res.company'
        )._company_default_get(
            cr, uid, 'account.analytic.line', context=context
        )
        vals_line['product_uom_id'] = vals['product_uom_id']
        vals_line['product_id'] = vals['product_id']
        vals_line['version_id'] = version_id
        vals_line['journal_id'] = self._getAnalyticPlanJournal(
            cr, uid, context=context
        ),
        vals_line['general_account_id'] = vals['general_account_id']
        vals_line['user_id'] = vals['user_id']

        new_line_plan_id = line_plan_obj.create(
            cr, uid, vals=vals_line, context=context
        )

        vals['analytic_line_plan'] = new_line_plan_id

        analytic_timesheet = super(hr_analytic_timesheet, self).create(
            cr, uid, vals, *args, **kwargs
        )

        return analytic_timesheet

    def write(self, cr, uid, ids, vals, context=None):
        if context is None:
            context = {}
        line_plan_obj = self.pool.get('account.analytic.line.plan')
        vals_line = {}

        if 'name' in vals:
            vals_line['name'] = vals['name']
        if 'date' in vals:
            vals_line['date'] = vals['date']
        if 'amount' in vals:
            vals_line['amount'] = vals['amount']
            vals_line['amount_currency'] = vals['amount']
        if 'unit_amount' in vals:
            vals_line['unit_amount'] = vals['unit_amount']
        if 'account_id' in vals:
            vals_line['account_id'] = vals['account_id']
        if 'company_id' in vals:
            vals_line['company_id'] = vals['company_id']
        if 'product_uom_id' in vals:
            vals_line['product_uom_id'] = vals['product_uom_id']
        if 'product_id' in vals:
            vals_line['product_id'] = vals['product_id']
        if 'general_account_id' in vals:
            vals_line['general_account_id'] = vals['general_account_id']
        if 'user_id' in vals:
            vals_line['user_id'] = vals['user_id']

        if isinstance(ids, (long, int)):
            ids = [ids]

        for hr_timesheet in self.browse(cr, uid, ids, context=context):
            if hr_timesheet.analytic_line_plan:
                line_plan_obj.write(
                    cr, uid,
                    [hr_timesheet.analytic_line_plan.id],
                    vals_line,
                    context
                )
            else:
                new_ana_line_plan = line_plan_obj.create(
                    cr, uid, vals_line, context=context
                )
                vals['analytic_line_plan'] = new_ana_line_plan

        return super(hr_analytic_timesheet, self).write(
            cr, uid, ids, vals, context=context
        )

    def unlink(self, cr, uid, ids, context=None):
        toremove = {}
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.analytic_line_plan:
                toremove[obj.analytic_line_plan.id] = True
        if toremove:
            self.pool.get('account.analytic.line.plan').unlink(
                cr, uid, toremove.keys(), context=context
            )
        return super(hr_analytic_timesheet, self).unlink(
            cr, uid, ids, context=context
        )

hr_analytic_timesheet()
