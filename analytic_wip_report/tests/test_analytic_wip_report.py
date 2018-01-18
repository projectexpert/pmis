# -*- coding: utf-8 -*-
# Copyright 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


class TestAnalyticWipReport(common.TransactionCase):
    def setUp(self):
        super(TestAnalyticWipReport, self).setUp()
        self.Project = self.env['project.project']
        self.AnalyticAccountObject = self.env['account.analytic.account']
        self.account_invoice = self.env['account.invoice']
        self.account_model = self.env['account.account']
        self.account_invoice_line = self.env['account.invoice.line']

        self.partner = self.env.ref('base.res_partner_2')
        self.receivable = self.env.ref('account.data_account_type_receivable')
        self.analytic_plan_version =\
            self.env.ref('analytic_plan.analytic_plan_version_P02')

        self.AnalyticAccount_parent = self.AnalyticAccountObject.create({
            'name': 'AnalyticAccount Parent for Test',
            'partner_id': self.partner.id
        })

        self.AnalyticAccount_child = self.AnalyticAccountObject.create({
            'name': 'AnalyticAccount Child for Test',
            'parent_id': self.AnalyticAccount_parent.id,
            'active_analytic_planning_version': self.analytic_plan_version.id,
            'account_class': 'project',
        })

        self.project_id = self.Project.create({
            'name': 'Test Project',
            'parent_id': self.AnalyticAccount_child.id,
            'account_class': 'project',
            'active_analytic_planning_version': self.analytic_plan_version.id,
        })

    def test_invoice(self):
        self.invoice_account = self.account_model.search(
            [('user_type_id', '=', self.receivable.id)], limit=1)
        self.invoice_line = self.account_invoice_line.create({
            'name': 'Test invoice line',
            'account_id': self.invoice_account.id,
            'quantity': 2,
            'price_unit': 100,
            'account_analytic_id': self.project_id.parent_id.id
        })
        self.invoice = self.account_invoice.create({
            'partner_id': self.partner.id,
            'account_id': self.invoice_account.id,
            'invoice_line_ids': [(6, 0, [self.invoice_line.id])]
        })
        self.invoice.action_invoice_open()
        self.assertEquals(self.project_id.parent_id.credit,
                          self.project_id.parent_id.balance)

    def test_check_wip_report(self):
        res = self.project_id.parent_id._compute_wip_report()
        project = res.get(self.project_id.parent_id.id)
        self.assertEquals(project.get('earned_revenue'), 0)
        self.assertEquals(project.get('total_value'), 0)
        self.assertEquals(project.get('actual_costs'), 0)
        self.assertEquals(project.get('total_estimated_costs'), 0)
