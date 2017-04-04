# -*- coding: utf-8 -*-
# © 2014-17 Eficent Business and IT Consulting Services S.L.
# © 2016 Matmoz d.o.o.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp.osv import fields, osv


class stock_picking(osv.osv):

    _inherit = "stock.picking"

    _columns = {
        'analytic_account_ids': fields.related(
            'move_lines', 'analytic_account_id', type='many2many',
            relation='account.analytic.account', string='Analytic Account',
            readonly=True),
        'analytic_account_user_ids': fields.related('move_lines',
                                                    'analytic_account_user_id',
                                                    type='many2many',
                                                    relation='res.users',
                                                    string='Project Manager',
                                                    readonly=True),
    }
