# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# (Jordi Ballester Alomar)
#
# © 2016 Matmoz d.o.o.
# (Matjaž Mozetič)
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class AccountAnalyticPlanJournal(models.Model):

    _name = 'account.analytic.plan.journal'
    _description = 'Analytic Journal Plan'

    name = fields.Char(
        'Planning Journal Name', required=True
    )
    code = fields.Char(
        'Planning Journal Code'
    )
    active = fields.Boolean(
        'Active',
        help="If the active field is set to False, "
             "it will allow you to hide the analytic "
             "journal without removing it.",
        default=True
    )
    type = fields.Selection(
        [
            ('sale', 'Sale'),
            ('purchase', 'Purchase'),
            ('cash', 'Cash'),
            ('general', 'General'),
            ('situation', 'Situation')
        ],
        'Type',
        required=True,
        help="Gives the type of the analytic "
             "journal. When it needs for a document "
             "(eg: an invoice) to create analytic "
             "entries, OpenERP will look  for a "
             "matching journal of the same type.",
        default='general'
    )
    line_ids = fields.One2many(
        'account.analytic.line.plan',
        'journal_id',
        'Lines'
    )
    company_id = fields.Many2one(
        'res.company',
        'Company',
        required=True,
        default=lambda self:
            self.env['res.users'].browse(self._uid).company_id.id)
    analytic_journal = fields.Many2one(
        'account.analytic.journal',
        'Actual Analytic journal',
        required=False
    )
