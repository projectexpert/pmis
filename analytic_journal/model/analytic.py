# -*- coding: utf-8 -*-
# Copyright 2015 Odoo SA
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lpgl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    journal_id = fields.Many2one(
        'account.analytic.journal', 'Analytic Journal', required=True,
        ondelete='restrict', index=True)


class AccountAnalyticJournal(models.Model):
    _name = 'account.analytic.journal'
    _description = 'Analytic Journal'

    name = fields.Char(string='Journal Name', required=True)
    code = fields.Char(string='Short Code', size=5, required=True)
    type = fields.Selection([
        ('sale', 'Sale'),
        ('purchase', 'Purchase'),
        ('cash', 'Cash'),
        ('bank', 'Bank'),
        ('general', 'Miscellaneous')], required=True,
        help="Select 'Sale' for customer invoices journals. Select 'Purchase'"
             " for vendor bills journals. Select 'Cash' or 'Bank' for "
             "journals that are used in customer or vendor payments."
             "Select 'General' for miscellaneous operations journals.")

    line_ids = fields.One2many('account.analytic.line', 'journal_id',
                               'Lines', copy=False)
    company_id = fields.Many2one(
        comodel_name='res.company',
        default=lambda self: self._get_default_company()
    )

    @api.model
    def find_journal(self, vals=None):
        if vals and vals.get('code', False):
            self.search([('code', '=', vals['code'])])
        return None

    @api.model
    def _prepare_analytic_journal(self, vals):
        if vals.get('type') and vals.get('name') and vals.get('code'):
            vals = {
                'type': vals['type'],
                'name': _(vals['name']),
                'code': vals['code']}
        else:
            raise ValidationError(_('Cannot create an analytic journal'))
        return vals

    def _get_default_company(self):
        return self.env.user.company_id.id


class AccountJournal(models.Model):
    _inherit = "account.journal"

    analytic_journal_id = fields.Many2one(
        'account.analytic.journal',
        'Analytic Journal',
        help="Journal for analytic entries")


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.multi
    def _prepare_analytic_line(self):
        self.ensure_one()
        res = super(AccountMoveLine, self)._prepare_analytic_line()
        if not self.journal_id.analytic_journal_id:
            raise ValidationError(_("Please define an analytic journal for "
                                    "journal %s" % self.journal_id.name))
        res[0]['journal_id'] = self.journal_id.analytic_journal_id.id
        return res


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def invoice_line_move_line_get(self):
        res = super(AccountInvoice, self).invoice_line_move_line_get()
        for data in res:
            if data.get('analytic_line_ids', False) and data.get('invoice_id'):
                aj = self.browse(
                    data['invoice_id']).journal_id.analytic_journal_id.id
                for line in data['analytic_line_ids']:
                    line[2]['journal_id'] = aj
        return res
