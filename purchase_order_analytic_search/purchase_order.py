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

from osv import fields, osv


class purchase_order(osv.osv):
    
    _inherit = "purchase.order"

    _columns = {
        'account_analytic_ids': fields.related('order_line',
                                               'account_analytic_id',
                                               type='many2many',
                                               relation='account.analytic.account',
                                               string='Analytic Account',
                                               readonly=True),
        'account_analytic_user_ids': fields.related('order_line',
                                                    'account_analytic_user_id',
                                                    type='many2many',
                                                    relation='res.users',
                                                    string='Project Manager',
                                                    readonly=True),
    }    
    
purchase_order()