# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. <contact@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Change Management Project Proposal',
    'version': '8.0.1.0.2',
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
    'active': False,
}
