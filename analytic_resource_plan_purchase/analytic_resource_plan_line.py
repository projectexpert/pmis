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
import decimal_precision as dp
from osv import fields, osv


class analytic_resource_plan_line(osv.osv):
    
    _inherit = 'analytic.resource.plan.line'

    _columns = {
        'order_line_ids': fields.many2many('purchase.order.line',
                                           'analytic_resource_plan_order_line_rel',
                                           'order_line_id',
                                           'analytic_resource_plan_line_id'),
    }

analytic_resource_plan_line()