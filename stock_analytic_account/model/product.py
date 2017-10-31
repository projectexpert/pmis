# -*- coding: utf-8 -*-
# Copyright 2014-17 Eficent Business and IT Consulting Services S.L.
# Copyright 2016 Matmoz d.o.o.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.tools.float_utils import float_round


class Product(models.Model):

    _inherit = "product.product"

    @api.multi
    def _compute_quantities_dict(self, lot_id, owner_id, package_id,
                                 from_date=False, to_date=False):
        domain_quant_loc, domain_move_in_loc, domain_move_out_loc =\
            self._get_domain_locations()
        domain_quant = [('product_id', 'in', self.ids)] + domain_quant_loc
        dates_in_the_past = False
        if to_date and to_date < fields.Datetime.now():
            dates_in_the_past = True

        domain_move_in = [('product_id', 'in', self.ids)] + domain_move_in_loc
        domain_move_out = [('product_id', 'in', self.ids)
                           ] + domain_move_out_loc
        if lot_id:
            domain_quant += [('lot_id', '=', lot_id)]
        if owner_id:
            domain_quant += [('owner_id', '=', owner_id)]
            domain_move_in += [('restrict_partner_id', '=', owner_id)]
            domain_move_out += [('restrict_partner_id', '=', owner_id)]
        if package_id:
            domain_quant += [('package_id', '=', package_id)]
        if dates_in_the_past:
            domain_move_in_done = list(domain_move_in)
            domain_move_out_done = list(domain_move_out)
        if from_date:
            domain_move_in += [('date', '>=', from_date)]
            domain_move_out += [('date', '>=', from_date)]
        if to_date:
            domain_move_in += [('date', '<=', to_date)]
            domain_move_out += [('date', '<=', to_date)]
        # START OF stock_analytic_account
        if self._context.get('analytic_account_id'):
            analytic_domain = ('analytic_account_id', '=',
                               self._context['analytic_account_id'])
            domain_move_in.append(analytic_domain)
            domain_move_out.append(analytic_domain)
            domain_quant.append(('analytic_account_id', '=',
                                 self._context['analytic_account_id']))
        # END OF stock_analytic_account
        Move = self.env['stock.move']
        Quant = self.env['stock.quant']
        domain_move_in_todo = [('state', 'not in', ('done', 'cancel', 'draft'))
                               ] + domain_move_in
        domain_move_out_todo = [('state', 'not in', ('done', 'cancel', 'draft')
                                 )] + domain_move_out
        moves_in_res =\
            dict((item['product_id'][0], item['product_qty']
                  ) for item in Move.read_group(domain_move_in_todo,
                                                ['product_id', 'product_qty'],
                                                ['product_id']))
        moves_out_res =\
            dict((item['product_id'][0], item['product_qty']
                  ) for item in Move.read_group(domain_move_out_todo,
                                                ['product_id', 'product_qty'],
                                                ['product_id']))
        quants_res =\
            dict((item['product_id'][0], item['qty']
                  ) for item in Quant.read_group(domain_quant,
                                                 ['product_id', 'qty'],
                                                 ['product_id']))
        if dates_in_the_past:
            # Calculate the moves that were done before now to calculate back
            # in time (as most questions will be recent ones)
            domain_move_in_done =\
                [('state', '=', 'done'), ('date', '>', to_date)
                 ] + domain_move_in_done
            domain_move_out_done =\
                [('state', '=', 'done'), ('date', '>', to_date)
                 ] + domain_move_out_done
            moves_in_res_past =\
                dict((item['product_id'][0], item['product_qty']
                      ) for item in Move.read_group(domain_move_in_done,
                                                    ['product_id',
                                                     'product_qty'],
                                                    ['product_id']))
            moves_out_res_past =\
                dict((item['product_id'][0], item['product_qty']
                      ) for item in Move.read_group(domain_move_out_done,
                                                    ['product_id',
                                                     'product_qty'],
                                                    ['product_id']))
        res = dict()
        for product in self.with_context(prefetch_fields=False):
            res[product.id] = {}
            if dates_in_the_past:
                qty_available =\
                    quants_res.get(product.id, 0.0) - moves_in_res_past.\
                    get(product.id, 0.0) + moves_out_res_past.get(product.id,
                                                                  0.0)
            else:
                qty_available = quants_res.get(product.id, 0.0)
            res[product.id]['qty_available'] =\
                float_round(qty_available,
                            precision_rounding=product.uom_id.rounding)
            res[product.id]['incoming_qty'] =\
                float_round(moves_in_res.get(product.id, 0.0),
                            precision_rounding=product.uom_id.rounding)
            res[product.id]['outgoing_qty'] =\
                float_round(moves_out_res.get(product.id, 0.0),
                            precision_rounding=product.uom_id.rounding)
            res[product.id]['virtual_available'] =\
                float_round(qty_available + res[product.id]['incoming_qty'] -
                            res[product.id]['outgoing_qty'],
                            precision_rounding=product.uom_id.rounding)
        return res
