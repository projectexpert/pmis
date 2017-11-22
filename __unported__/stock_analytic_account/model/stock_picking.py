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
from openerp.osv import fields, osv


class stock_picking(osv.osv):

    _inherit = "stock.picking"

    _columns = {
        'analytic_account_ids': fields.related(
            'move_lines', 'analytic_account_id', type='many2many',
            relation='account.analytic.account', string='Analytic Account',
            readonly=True
        ),
        'analytic_account_user_ids': fields.related(
            'move_lines',
            'analytic_account_user_id',
            type='many2many',
            relation='res.users',
            string='Project Manager',
            readonly=True
        ),
    }
