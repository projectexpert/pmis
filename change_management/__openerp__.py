# -*- coding: utf-8 -*-
# Copyright (C) 2015 Matmoz d.o.o. (<http://www.matmoz.si>).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Change Management',
    'version': '8.0.3.0.6',
    'author': 'Matmoz d.o.o., '
              'Project Expert Team',
    'contributors': [
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'summary': 'Change Management integrated with Stakeholders Requirements',
    'depends': ['project', 'project_charter', 'project_wbs'],
    'data': [
        'data/change_management_data.xml',
        'data/change_management_sequence.xml',
        'security/ir.model.access.csv',
        'view/project_task_view.xml',
        'view/change_management_view.xml',
        'view/change_management_category_view.xml',
        'view/change_management_proximity_view.xml',
        'view/change_management_menus.xml'
    ],
    'demo': ['demo/change_management_demo.xml'],
    'test': ['test/test_change_management.yml'],
    'installable': True,
    'application': True,
    'active': False,
}
