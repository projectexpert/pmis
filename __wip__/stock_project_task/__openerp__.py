# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Stock Project Task",
    "summary": "Adds an project task in stock move",
    'version': '8.0.1.0.0',
    'author':   'Eficent, '
                'Project Expert Team',
    'website': 'http://project.expert',
    "category": "Warehouse Management",
    "license": "AGPL-3",
    "depends": [
        "stock_project",
    ],
    "data": [
        "views/stock_move_views.xml",
        "views/stock_inventory_views.xml",
    ],
    'installable': True,
    'active': False,
}
