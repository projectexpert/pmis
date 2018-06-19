# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Luxim d.o.o.
# Copyright 2017 Matmoz d.o.o.
# Copyright 2017 Deneroteam.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


class TestAnalyticResourcePlan(common.SavepointCase):

    def setUp(cls):
        super(TestAnalyticResourcePlan, cls).setUp()
        cls.project = cls.env['project.project'].create(
            {'name': 'Test project',
             'code': '0001'})
        cls.parent_account = cls.project.analytic_account_id
        cls.plan_version = cls.env.ref(
            'analytic_plan.analytic_plan_version_P02')
        cls.plan_version.write({'default_resource_plan': True})
        cls.parent_account.write({
            'active_analytic_planning_version': cls.plan_version.id})
        cls.product = cls.env.ref('product.product_product_6')
        cls.anal_journal = cls.env['account.analytic.journal'].create(
            {'name': 'Expenses',
             'code': 'EX',
             'type': 'purchase'}
        )
        cls.plan_expenses = cls.env['account.analytic.plan.journal'].create(
            {'name': 'expenses',
             'code': 'EXP',
             'journal_id': cls.anal_journal.id,
             }
        )
        cls.resource_plan_line = cls.env['analytic.resource.plan.line'].create(
            {'product_id': cls.product.id,
             'product_uom_id': cls.product.uom_id.id,
             'name': 'fetch',
             'account_id': cls.parent_account.id,
             'unit_amount': 1.0,
             }
        )
        cls.product.write(
            {'expense_analytic_plan_journal_id': cls.plan_expenses.id,})

    def test_confirm(cls):
        cls.resource_plan_line.action_button_confirm()
        cls.assertEqual(cls.resource_plan_line.state, 'confirm')
