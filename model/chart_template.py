# -*- coding: utf-8 -*-
# Copyright 2015 Odoo SA
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lpgl.html).

from odoo import api, models


class AccountChartTemplate(models.Model):
    _inherit = "account.chart.template"

    @api.multi
    def _prepare_all_journals(
            self, acc_template_ref, company, journals_dict=None):
        res = super(AccountChartTemplate, self)._prepare_all_journals(
            acc_template_ref, company, journals_dict=journals_dict)
        anal_obj = self.env['account.analytic.journal']
        for journal in res:
            analytic_journal = anal_obj.find_journal(journal)
            if not analytic_journal:
                vals = anal_obj._prepare_analytic_journal(journal)
                analytic_journal = anal_obj.create(vals)
            journal.update(analytic_journal_id=analytic_journal.id)
        return res
