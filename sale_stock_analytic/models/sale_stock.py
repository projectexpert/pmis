# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields, orm


class SaleOrder(orm.Model):
    _inherit = "sale.order"

    def _prepare_order_line_move(self, cr, uid, order, line, picking_id,
                                 date_planned, context=None):

        res = super(SaleOrder, self)._prepare_order_line_move(
            cr, uid, order, line, picking_id, date_planned, context=context
        )
        res['analytic_account_id'] = (
            line.order_id and
            line.order_id.project_id and
            line.order_id.project_id.id
        )
        return res
