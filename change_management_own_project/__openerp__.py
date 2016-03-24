# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. <contact@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Change Management Own Project',
    'version': '8.0.1.0.0',
    'author':   'Eficent Business and IT Consulting Services S.L.',
    'website': 'www.eficent.com',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'summary': 'Creates a project for each Change, child of the project '
               'indicated.',
    'depends': ['change_management'],
    'data': [
        'views/change_management_view.xml',
    ],
    'installable': True,
    'application': True,
    'active': False,
}
