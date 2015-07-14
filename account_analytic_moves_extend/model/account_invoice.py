# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#              Jordi Ballester Alomar <jordi.ballester@eficent.com>
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


class account_invoice(osv.osv):

    _inherit = "account.invoice"

    def _get_analytic_lines(self, cr, uid, id, context=None):

        if context is None:
            context = {}
        inv = self.browse(cr, uid, id)
        cur_obj = self.pool.get('res.currency')

        iml = self.pool.get('account.invoice.line').move_line_get(cr, uid, inv.id, context=context)

        return iml

account_invoice()
