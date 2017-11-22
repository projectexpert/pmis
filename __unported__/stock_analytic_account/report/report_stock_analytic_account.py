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

from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
from openerp.tools.sql import drop_view_if_exists


class stock_report_analytic_account(orm.Model):
    _name = "stock.report.analytic.account"
    _description = "Stock report by analytic account"
    _auto = False
    _columns = {
        'qty': fields.float(
            'Quantity in ref UoM',
            help="Quantity expressed in the reference UoM",
            readonly=True),
        'location_id': fields.many2one('stock.location', 'Location',
                                       readonly=True, select=True),
        'usage': fields.selection([('supplier', 'Supplier Location'),
                                   ('view', 'View'),
                                   ('internal', 'Internal Location'),
                                   ('customer', 'Customer Location'),
                                   ('inventory', 'Inventory'),
                                   ('procurement', 'Procurement'),
                                   ('production', 'Production'),
                                   ('transit', 'Transit Location for '
                                               'Inter-Companies Transfers')],
                                  'Location Type', readonly=True),
        'product_id': fields.many2one('product.product', 'Product',
                                      readonly=True, select=True),
        'analytic_account_id': fields.many2one('account.analytic.account',
                                               'Analytic Account',
                                               readonly=True, select=True),
        'analytic_reserved': fields.boolean('Stock reserved for the '
                                            'Analytic Account',
                                            readonly=True, select=True),
    }

    def init(self, cr):
        drop_view_if_exists(cr, 'stock_report_analytic_account')
        cr.execute("""
            create or replace view stock_report_analytic_account as (
                select max(id) as id,
                    location_id,
                    usage,
                    product_id,
                    analytic_account_id,
                    analytic_reserved,
                    sum(qty) as qty
                from (
                    select -max(sm.id) as id,
                        sm.location_id,
                        sl.usage,
                        sm.product_id,
                        sm.analytic_account_id,
                        sm.analytic_reserved,
                        -sum(sm.product_qty /uo.factor) as qty
                    from stock_move as sm
                    left join stock_location sl
                        on (sl.id = sm.location_id)
                    left join product_uom uo
                        on (uo.id=sm.product_uom)
                    where state = 'done'
                    group by sm.location_id, sl.usage, sm.product_id,
                    sm.product_uom,
                    sm.analytic_account_id,
                    sm.analytic_reserved
                    union all
                    select max(sm.id) as id,
                        sm.location_dest_id as location_id,
                        sl.usage,
                        sm.product_id,
                        sm.analytic_account_id,
                        sm.analytic_reserved,
                        sum(sm.product_qty /uo.factor) as qty
                    from stock_move as sm
                    left join stock_location sl
                        on (sl.id = sm.location_dest_id)
                    left join product_uom uo
                        on (uo.id=sm.product_uom)
                    where sm.state = 'done'
                    group by sm.location_dest_id, sl.usage, sm.product_id,
                    sm.product_uom, sm.analytic_account_id,
                    sm.analytic_reserved
                ) as report
                group by location_id, usage, product_id,
                analytic_account_id, analytic_reserved
            )""")

    def unlink(self, cr, uid, ids, context=None):
        raise osv.except_osv(_('Error!'), _('You cannot delete any record!'))
