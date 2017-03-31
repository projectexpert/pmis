# -*- coding: utf-8 -*-
# © 2014-17 Eficent Business and IT Consulting Services S.L.
# © 2016 Matmoz d.o.o.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Analytic Account Cost Category',
    'version': '9.0.1.0.0',
    'summary': 'Adds the cost category to analytic accounts.',
    'author':   'Eficent, '
                'Project Expert Team',
    'contributors': [
        'Jordi Ballester <jordi.ballester@eficent.com>',
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'depends': ['account', 'analytic'],
    'data': [
        'views/account_analytic_account_view.xml',
    ],
    'demo': [

    ],
    'test': [
    ],
    'installable': True,
    'active': False,
    'certificate': '',
}
