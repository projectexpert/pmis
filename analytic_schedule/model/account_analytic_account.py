# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    @api.multi
    @api.depends('child_ids', 'project_ids')
    def _compute_scheduled_dates(self):
        """Obtains the earliest and latest dates of the children."""
        for analytic in self:
            start_dates = []
            end_dates = []
            if not analytic.child_ids:
                for project in analytic.project_ids:
                    if project.date_start:
                        start_dates.append(project.date_start)
                    if project.date:
                        end_dates.append(project.date)
            for child in analytic.child_ids:
                for project in child.project_ids:
                    if project.date_start:
                        start_dates.append(project.date_start)
                    if project.date:
                        end_dates.append(project.date)
            min_start_date = False
            max_end_date = False
            if start_dates:
                min_start_date = min(start_dates)
            if end_dates:
                max_end_date = max(end_dates)
            analytic.date_start = min_start_date
            analytic.date = max_end_date
        return True

    date_start = fields.Date(compute=_compute_scheduled_dates)
    date = fields.Date(compute=_compute_scheduled_dates)
