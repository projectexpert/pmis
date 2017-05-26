# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Change Management Project Proposal',
    'version': '9.0.1.0.0',
    'author': 'Eficent Business and IT Consulting Services S.L., '
              'Project Expert Team',
    'contributors': [
        'Jordi Ballester <jordi.ballester@eficent.com>',
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'website': 'www.eficent.com',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'summary': 'Proposes a project for each Change Request, child of the'
               'indicated source project.',
    'depends': ['change_management'],
    'data': [
        'views/change_management_view.xml',
    ],
    'installable': True,
    'application': True,
}
