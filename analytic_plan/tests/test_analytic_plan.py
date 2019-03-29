# -*- coding: utf-8 -*-
# Copyright 2015 Eficent Business and IT Consulting Services S.L.
# (Jordi Ballester Alomar)
# Copyright 2016 Matmoz d.o.o.
# (Matjaž Mozetič)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase
from odoo import fields


class TestAnalyticPlan(TransactionCase):

    def setUp(self):
        super(TestAnalyticPlan, self).setUp()
        self.analytic_line_plan_obj = self.env['account.analytic.line.plan']
        self.analytic_account_obj = self.env['account.analytic.account']
        self.analytic_line_obj = self.env['account.analytic.line']
        self.analytic_plan_journal_obj =\
            self.env['account.analytic.plan.journal']
        self.account_obj = self.env['account.account']
        self.partner = self.env.ref('base.res_partner_2')
        self.product_id = self.env.ref('product.consu_delivery_03')
        self.product1_id = self.env.ref('product.product_product_24')
        self.analytic_plan_version =\
            self.env.ref('analytic_plan.analytic_plan_version_P02')
        self.revenue = self.env.ref('account.data_account_type_revenue')
        self.general_account_id = self.account_obj.\
            search([('user_type_id', '=', self.revenue.id)], limit=1)

        self.analytic_parent1 = self.analytic_account_obj.create({
            'name': 'Parent Analytic Account',
            'active_analytic_planning_version': self.analytic_plan_version.id,
            'partner_id': self.partner.id
        })

        self.analytic_account = self.analytic_account_obj.create({
            'name': 'Test Analytic Account',
            'active_analytic_planning_version': self.analytic_plan_version.id,
            'parent_id': self.analytic_parent1.id
        })

        self.analytic_plan_journal = self.analytic_plan_journal_obj.create({
            'name': 'Sale',
            'type': 'sale',
            'code': 'SAL',
            'active': True
        })

        self.analytic_line_plan = self.analytic_line_plan_obj.create({
            'name': self.product_id.name,
            'date': fields.Date.today(),
            'amount': 100,
            'unit_amount': 10,
            'account_id': self.analytic_account.id,
            'partner_id': self.partner.id,
            'journal_id': self.analytic_plan_journal.id,
            'version_id': self.analytic_plan_version.id,
            'product_id': self.product_id.id,
            'general_account_id': self.general_account_id.id,
        })

        self.analytic_line = self.analytic_line_obj.create({
            'account_id': self.analytic_account.id,
            'name': 'Test',
            'unit_amount': 11,
            'date': fields.Date.today(),
            'product_id': self.product1_id.id
        })

    def test_analytic_plan(self):
        self.balance_plan = self.analytic_account.\
            credit_plan - self.analytic_account.debit_plan
        self.assertEquals(self.analytic_account.balance_plan,
                          self.balance_plan)
