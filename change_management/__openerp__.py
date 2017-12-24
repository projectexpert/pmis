# -*- coding: utf-8 -*-
# Copyright (C) 2017 Matmoz d.o.o. (<http://www.matmoz.si>).
# Copyright (C) 2018 Luxim d.o.o. (<https://www.luxim.si>).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Change Management',
    'version': '8.0.3.2.0',
    'author': 'Matmoz d.o.o., '
              'Project Expert Team',
    'contributors': [
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'website': 'http://project.expert',
    'category': 'Advanced Project Management',
    'license': 'AGPL-3',
    'summary': 'Change Management and change based (agile) life cycle',
    'depends': [
        'project_charter',
        'analytic_billing_plan',
        'project_stage_state'
    ],
    'data': [
        'data/change_management_data.xml',
        'data/change_management_sequence.xml',
        'security/ir.model.access.csv',
        'view/project_task_view.xml',
        'view/change_management_view.xml',
        'view/change_management_category_view.xml',
        'view/change_management_proximity_view.xml',
        'view/change_management_menus.xml',
        'view/billing_plan_view.xml'
    ],
    'demo': ['demo/change_management_demo.xml'],
    'test': [],
    'installable': True,
    'application': True,
    'active': False,
}
