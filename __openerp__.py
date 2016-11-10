# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# (Jordi Ballester Alomar)
#
# © 2016 Matmoz d.o.o.
# (Matjaž Mozetič)
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Analytic Resource Planning',
    'version': '8.0.2.0.3',
    'author':   'Eficent, '
                'Matmoz, '
                'Project Expert Team',
    'contributors': [
        'Jordi Ballester <jordi.ballester@eficent.com>',
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'depends': ['account', 'purchase', 'analytic_plan'],
    'data': [
        'view/account_analytic_plan_version_view.xml',
        'view/analytic_resource_plan_view.xml',
        'view/analytic_account_view.xml',
        'view/product_view.xml',
        'view/project_view.xml',
        'view/resource_plan_default.xml',
        'security/ir.model.access.csv',

    ],
    'demo': [

    ],
    'test': [
    ],
    'installable': True,
    'active': False,
    'certificate': '',
}
