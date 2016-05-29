# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright: (C) 2012 - Mentis d.o.o., Dravograd
#    Updated: (C) 2014 - Matmoz d.o.o., Ljubljana
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name": "Slovenian - Accounting - Updated",
    "version": "1.2",
    "author": "Mentis d.o.o., "
              "Matmoz d.o.o.",
    "website": "http://www.matmoz.si",
    "category": "Localization/Account Charts",
    "depends": [
        "account",
        "base_iban",
        "base_vat",
        "account_chart",
        "account_cancel"
    ],
    "description": "Kontni načrt za gospodarske družbe - verzija 2014",
    'license': "AGPL-3",
    'contributors': [
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    "data": [
        "data/account.account.type.csv",
        "data/account.account.template.csv",
        "data/account.tax.code.template.csv",
        "data/account.chart.template.csv",
        "data/account.tax.template.csv",
        "data/account.fiscal.position.template.csv",
        "data/account.fiscal.position.account.template.csv",
        "data/account.fiscal.position.tax.template.csv",
        "l10n_si_wizard.xml"
    ],
    'auto_install': False,
    "installable": True,
}
