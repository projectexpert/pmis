# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Analytic Schedule",
    "version": "10.0.2.0.0",
    "summary": "Automatically computes start and end dates for analytic "
               "accounts based on the earliest start and latest finish date "
               "of the children.",
    "author": "Eficent",
    "website": "www.eficent.com",
    "category": "Generic Modules/Projects & Services",
    "depends": ["analytic", "account_analytic_parent"],
    "data": ['views/analyltic_account_view.xml'],
    'installable': True,
}
