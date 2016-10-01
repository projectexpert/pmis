# -*- coding: utf-8 -*-
# Copyright (C) 2015 Matmoz d.o.o. (<http://www.matmoz.si>).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import fields

def migrate(cr, version):
    cr.execute(
        'SELECT id, stakeholder_id_premigration FROM change_management_change'
    )
    for record_id, old_proposer in cr.fetchall():
        new_proposer = None
