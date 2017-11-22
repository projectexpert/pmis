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


class sale_order_line(osv.osv):

    _inherit = "sale.order.line"

    _columns = {
        'project_id': fields.related(
            'order_id', 'project_id',
            type='many2one',
            relation='account.analytic.account',
            string='Analytic Account',
            readonly=True
        ),

        'project_user_id': fields.related(
            'order_id', 'project_user_id',
            type='many2one',
            relation='res.users',
            string='Project Manager',
            readonly=True
        ),
    }

sale_order_line()
