#    Copyright 2015 MATMOZ, Slovenia (Matjaž Mozetič)
#    Copyright 2015 EFICENT (Jordi Ballester Alomar)
#    Copyright 2018 LUXIM, Slovenia (Matjaž Mozetič)
#    Together as the Project Expert Team
#    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestAnalyticDeliverablePlan(common.SavepointCase):

    def setUp(cls):
        super(TestAnalyticDeliverablePlan, cls).setUp()
        cls.project = cls.env['project.project'].create(
            {'name': 'Test project',
             'code': '0001'})
        cls.account_id = cls.project.analytic_account_id
        cls.product = cls.env['product.product'].create({'name': 'SP'})
        cls.anal_journal = cls.env['account.analytic.journal'].create(
            {'name': 'Expenses',
             'code': 'EX',
             'type': 'purchase'}
        )
        cls.plan_expenses = cls.env['account.analytic.plan.journal'].create(
            {'name': 'expenses',
             'code': 'EXP',
             'analytic_journal': cls.anal_journal.id,
             }
        )
        cls.deliverable_plan_line = cls.env['analytic.deliverable.plan.line'].create(
            {'product_id': cls.product.id,
             'product_uom_id': cls.product.uom_id.id,
             'name': 'fetch',
             'account_id': cls.account_id.id,
             'unit_amount': 1.0,
             }
        )
        cls.product.write(
            {'expense_analytic_plan_journal_id': cls.plan_expenses.id, })

    def test_plan(cls):
        cls.deliverable_plan_line.action_button_confirm()
        cls.assertEqual(cls.deliverable_plan_line.state, 'confirm')
        plan_line = cls.env['account.analytic.line.plan'].search(
            [('deliverable_plan_id', '=', cls.deliverable_plan_line.id)])
        cls.assertEqual(len(plan_line), 1, 'Wrong plan lines number')
        cls.deliverable_plan_line.action_button_draft()
        cls.assertEqual(cls.deliverable_plan_line.state, 'draft')
        plan_line = cls.env['account.analytic.line.plan'].search(
            [('deliverable_plan_id', '=', cls.deliverable_plan_line.id)])
        cls.assertEqual(len(plan_line), 0, 'Plan line not deleted')
