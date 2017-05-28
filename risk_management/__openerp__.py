# -*- coding: utf-8 -*-
# Copyright (C) 2011-2015 ValueDecision Ltd <http://www.valuedecision.com>.
# Copyright (C) 2015 Neova Health <http://www.neovahealth.co.uk>.
# Copyright (C) 2015 Matmoz d.o.o. <http://www.matmoz.si>.
# Copyright (C) 2017 Luxim d.o.o. <http://www.luxim.si>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Risk Management',
    'version': '8.0.2.1.6',
    'author':   'Neova Health ,'
                'Matmoz d.o.o., '
                'Project Expert Team',
    'website':  'http://www.matmoz.si',
    'category': 'Project Management',
    'license': "AGPL-3",
    'contributors': [
        'Neova Health',
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
        'Luxim d.o.o. <info@luxim.si>',
    ],
    'depends': ['project', 'project_charter'],
    'data': [
        'data/risk_management_data.xml',
        'data/risk_management_sequence.xml',
        'security/ir.model.access.csv',
        'view/project_task_view.xml',
        'view/project_charter_view.xml',
        'view/risk_management_view.xml',
        'view/risk_management_category_view.xml',
        'view/risk_management_category_response_view.xml',
        'view/risk_management_proximity_view.xml',
        'view/risk_management_menus.xml'
    ],
    'demo': ['demo/risk_management_demo.xml'],
    'test': ['test/test_risk_management.yml'],
    'installable': True,
    'application': True,
    'active': False,
}
