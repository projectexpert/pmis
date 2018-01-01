# -*- coding: utf-8 -*-

from datetime import date
from openerp import models, fields, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    date_invoice_creation = fields.Date(
        'Invoice Date',
        readonly=True,
        required=True,
        states={'draft': [('readonly', False)]},
        index=True,
        help="Date when invoice was created.",
        default=lambda *a: date.today().strftime('%Y-%m-%d')
    )

    date_invoice = fields.Date(
        'Debt Start Date',
        readonly=True,
        states={'draft': [('readonly', False)]},
        index=True,
        help="Date when debt relationship between customer and "
             "supplier started.",
        default=lambda *a: date.today().strftime('%Y-%m-%d')
    )

    date_invoice_recieved = fields.Date(
        'Date Recieved',
        readonly=True,
        required=True,
        states={'draft': [('readonly', False)]},
        index=True,
        help="Date when supplier invoice was recieved.",
        default=lambda *a: date.today().strftime('%Y-%m-%d')
    )

    _defaults = {
        'date_invoice_creation': lambda *a: date.today().strftime('%Y-%m-%d'),
        'date_invoice': lambda *a: date.today().strftime('%Y-%m-%d'),
        'date_invoice_recieved': lambda *a: date.today().strftime('%Y-%m-%d'),
    }

    @api.multi
    def action_date_assign(self):
        for inv in self:
            if not inv.date_due:
                super(AccountInvoice, self).action_date_assign()
        return True
