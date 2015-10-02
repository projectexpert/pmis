# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Eficent (<http://www.eficent.com/>)
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
from openerp.osv import fields, orm


class account_analytic_account(orm.Model):

    _inherit = "account.analytic.account"

    _columns = {
        'move_ids': fields.one2many(
            'stock.move', 'analytic_account_id',
            'Moves for this analytic account',
            readonly=True
        ),
        'use_reserved_stock': fields.boolean(
            'Use reserved stock',
            help="Stock with reference to this analytic account "
                 "is considered to be reserved."
        )
    }

    def copy(self, cr, uid, id, default=None, context=None):
        if context is None:
            context = {}
        if default is None:
            default = {}
        default['move_ids'] = []
        res = super(account_analytic_account, self).copy(
            cr, uid, id, default, context
        )
        return res
