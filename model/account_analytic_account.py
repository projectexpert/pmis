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

from openerp.osv import orm


class AccountAnalyticAccount(orm.Model):

    _inherit = 'account.analytic.account'

    def write(self, cr, uid, ids, vals, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]

        res = super(AccountAnalyticAccount, self).write(
            cr, uid, ids, vals, context=context)

        plan_line_obj = self.pool.get('analytic.resource.plan.line')
        if 'date' in vals and vals['date']:
            for analytic_account in self.browse(cr, uid, ids,
                                                context=context):
                plan_line_ids = plan_line_obj.search(
                    cr, uid, [('account_id', '=', analytic_account.id)],
                    context=context)
                if plan_line_ids:
                    plan_line_obj.write(
                        cr, uid, plan_line_ids, {'date': vals['date']})
        return res
