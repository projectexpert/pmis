# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError


class TestStockLocation(TransactionCase):

    def setUp(self):
        super(TestStockLocation, self).setUp()
        # Get registries
        self.user_model = self.env["res.users"]
        self.location_model = self.env["stock.location"]
        self.analytic_model = self.env["account.analytic.account"]
        self.move_model= self.env["stock.move"]

        self.yourcompany_loc = self.env.ref('stock.stock_location_stock')
        self.yourcompany_aa = self.env.ref('analytic.analytic_our_super_product')
        self.AA1 = self.create_analytic('AA1')
        self.AA2 = self.create_analytic('AA2')
        self.yourcompany_loc.write({'analytic_account_id': self.AA1.id})
        self.location1 = self.create_location(
            self.AA1, self.yourcompany_loc)

    def create_analytic(self, name):
        vals = {'name': name}
        analytic_id = self.analytic_model.create(vals)
        return analytic_id


    def create_location(self, analytic, parent):
        vals = {'name': analytic.name,
                'location_id': parent.id,
                'analytic_account_id': analytic.id
        }
        location_id = self.location_model.create(vals)
        return location_id

    def test_sublocation_analytic(self):
        """Test i cannot create sublocation with different AA"""
        with self.assertRaises(ValidationError):
            self.create_location(self.AA2, self.location1)
