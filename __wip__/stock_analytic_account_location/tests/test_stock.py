# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestStock(TransactionCase):

    def setUp(self):
        super(TestStock, self).setUp()
        self.location_model = self.env['stock.location']
        self.account_model = self.env['account.account']
        self.analytic_model = self.env['account.analytic.account']
        self.move_model= self.env['stock.move']
        self.yourcompany_loc = self.env.ref('stock.stock_location_stock')
        self.shelf_loc = self.env.ref('stock.stock_location_components')
        self.uom_id = self.env.ref('product.product_uom_unit')
        self.yourcompany_aa = self.env.ref(
            'analytic.analytic_commercial_marketing')
        self.AA1 = self.create_analytic('AA1')
        self.yourcompany_loc.write({'analytic_account_id': self.AA1.id})
        self.location1 = self.create_location(
            self.AA1, self.yourcompany_loc, 'internal')
        self.location2 = self.create_location(
            self.AA1, self.yourcompany_loc, 'customer')
        self.location3 = self.create_location(
            None, self.shelf_loc, 'internal')
        self.location4 = self.create_location(
            None, None, 'customer')
        self.product = self.env.ref('product.product_product_4')
        self.product_categ = self.env.ref('product.product_category_5')
        self.current_assets_type = self.env['account.account.type'].search(
            [('name', '=', 'Current Assets')], limit=1)
        self.cost_of_revenue = self.env['account.account.type'].search(
            [('name', '=', 'Cost of Revenue')], limit=1)
        self.current_liabilities_type = self.env['account.account.type'].search(
            [('name', '=', 'Current Liabilities')], limit=1)
        self.valuation_account = self.create_account(
            'Inventory', 5550, self.current_assets_type)
        self.stock_input_account = self.create_account(
            'GRNI', 5450, self.current_liabilities_type)
        self.stock_output_account = self.create_account(
            'COGS', 5350, self.cost_of_revenue)
        self.product_categ.update({
            'property_valuation': 'real_time',
            'property_stock_valuation_account_id': self.valuation_account.id,
            'property_stock_account_input_categ_id':
                self.stock_input_account.id,
            'property_stock_account_output_categ_id':
                self.stock_output_account.id,
        })
        self.product.update({
            'categ_id': self.product_categ.id,
        })

        self.move1 = self.create_move('out_aa', self.location1,
                                      self.location4)
        self.move2 = self.create_move('out', self.location3,
                                      self.location4)
        self.move3 = self.create_move('in_aa', self.location4,
                                      self.location1)
        self.move4 = self.create_move('in', self.location4,
                                      self.location3)

    def create_account(self, name, code, type):
            vals = {'name': name,
                    'code': code,
                    'user_type_id': type.id,
            }
            account = self.account_model.create(vals)
            return account

    def create_analytic(self, name):
            vals = {'name': 'name',
                    'parent_id': self.yourcompany_aa.id,
            }
            analytic = self.analytic_model.create(vals)
            return analytic


    def create_location(self, analytic, parent, usage):
        vals = {'name': analytic.name if analytic else 'no analytic',
                'location_id': parent.id if parent else None,
                'usage': usage,
                'analytic_account_id': analytic.id if analytic else None
        }
        location_id = self.location_model.create(vals)
        return location_id.id

    def create_move(self, name, src, dest):
        vals = {
            'name': name,
            'product_id': self.product.id,
            'product_uom_qty': 1.0,
            'product_uom': self.uom_id.id,
            'location_id': src,
            'location_dest_id': dest,
        }
        move = self.move_model.create(vals)
        move.action_done()
        return move

    def test_move_anaytic(self):
        """Test move have or not analytic account"""
        self.assertEqual(self.move1.analytic_account_id.id, self.AA1.id,
                         "Analytic account 1 should exist")
        self.assertEqual(self.move2.analytic_account_id.id, False,
                         "No analytic account should be in this move")
        self.assertEqual(self.move3.analytic_account_id.id, self.AA1.id,
                         "Analytic account 1 should exist")
        self.assertEqual(self.move4.analytic_account_id.id, False,
                         "No analytic account should be in this move")
