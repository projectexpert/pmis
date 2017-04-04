# -*- coding: utf-8 -*-
# © 2014-17 Eficent Business and IT Consulting Services S.L.
# © 2016 Matmoz d.o.o.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp.osv import fields, orm


class account_analytic_account(orm.Model):

    _inherit = "account.analytic.account"

    _columns = {
        'move_ids': fields.one2many('stock.move', 'analytic_account_id',
                                    'Moves for this analytic account',
                                    readonly=True)
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
