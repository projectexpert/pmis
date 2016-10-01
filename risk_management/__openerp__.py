# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Enterprise Management Solution
#    risk_management Module
#    Copyright (C) 2011-2015 ValueDecision Ltd <http://www.valuedecision.com>
#    Copyright (C) 2015 Neova Health <http://www.neovahealth.co.uk>.
#    Copyright (C) 2015 Matmoz d.o.o. <http://www.matmoz.si>.
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
    'name': 'Risk Management',
    'version': '8.0.2.1.5',
    'author':   'Neova Health ,'
                'Matmoz d.o.o., '
                'Project Expert Team',
    'website':  'http://www.matmoz.si',
    'category': 'Project Management',
    'license': "AGPL-3",
    'contributors': [
        'Neova Health',
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
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
