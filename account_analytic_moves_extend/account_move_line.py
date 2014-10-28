# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#              Eficent <contact@eficent.com>
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

from openerp.osv import fields, osv, orm
from openerp.tools.translate import _


class account_move_line(osv.osv):
    _inherit = "account.move.line"
    
    def create_analytic_lines(self, cr, uid, ids, context=None):
        acc_ana_line_obj = self.pool.get('account.analytic.line')
        for obj_line in self.browse(cr, uid, ids, context=context):
            #Only create analytic line if the associated account is Expense or Income.
            if obj_line.account_id.user_type and \
                            obj_line.account_id.user_type.report_type in ('income', 'expense'):
                if obj_line.analytic_account_id:
                    if not obj_line.journal_id.analytic_journal_id:
                        raise osv.except_osv(_('No Analytic Journal!'),
                                             _("You have to define an analytic journal "
                                               "on the '%s' journal!") % (obj_line.journal_id.name, ))
                    if obj_line.analytic_lines:
                        acc_ana_line_obj.unlink(cr, uid, [obj.id for obj in obj_line.analytic_lines])
                    vals_line = self._prepare_analytic_line(cr, uid, obj_line, context=context)
                    acc_ana_line_obj.create(cr, uid, vals_line)
        return True

account_move_line()