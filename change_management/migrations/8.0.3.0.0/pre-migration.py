# -*- coding: utf-8 -*-
# Copyright (C) 2015 Matmoz d.o.o. (<http://www.matmoz.si>).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

_name__ = u"Proposer becomes partner from stakeholder"

def migrate(cr, version):
    cr.execute(
        'ALTER TABLE change_management_change '
        'RENAME COLUMN stakeholder_id TO stakeholder_id_premigration'
    )
