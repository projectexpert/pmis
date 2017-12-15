# -*- coding: utf-8 -*-
#    Copyright 2017 Matmoz d.o.o. & Luxim d.o.o. (Matjaž Mozetič)
#    Copyright 2015 Eficent (Jordi Ballester Alomar)
#    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class AccountAnalyticPlanJournal(models.Model):

    _name = 'account.analytic.plan.journal'
    _description = 'Analytic Journal Plan'

    name = fields.Char(
        string='Planning Journal Name',
        required=True
    )
    code = fields.Char(
        string='Planning Journal Code'
    )
    active = fields.Boolean(
        string='Active',
        help="The active field set to False allows "
             "hiding the analytic "
             "journal without removing it.",
        default=True
    )
    type = fields.Selection(
        selection=[
            ('sale', 'Sale'),
            ('purchase', 'Purchase'),
            ('cash', 'Cash'),
            ('general', 'General'),
            ('situation', 'Situation')
        ],
        string='Type',
        required=True,
        help="Gives the type of the analytic "
             "journal. When a document needs "
             "(eg: an invoice) the creation of "
             "analytic entries, Odoo looks for a "
             "matching journal of the same type.",
        default='general'
    )
    line_ids = fields.One2many(
        comodel_name='account.analytic.line.plan',
        inverse_name='journal_id',
        string='Lines'
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        required=True,
        default=lambda self:
            self.env['res.users'].browse(self._uid).company_id.id
    )
    analytic_journal = fields.Many2one(
        comodel_name='account.analytic.journal',
        string='Actual Analytic journal',
        required=False
    )
