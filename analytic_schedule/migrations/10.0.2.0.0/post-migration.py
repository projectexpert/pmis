# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)
from openupgradelib import openupgrade


def store_dates(env):
    accounts = env['account.analytic.account'].search([('date', '=', False)])
    accounts._compute_scheduled_dates()


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    store_dates(env)
