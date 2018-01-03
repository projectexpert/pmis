# -*- coding: utf-8 -*-
#    Copyright 2015 Matmoz d.o.o. (Matjaž Mozetič)
#    Copyright 2015 Eficent (Jordi Ballester Alomar)
#    Copyright 2017 Deneroteam (Vijaykumar Baladaniya)
#    Copyright 2017 Luxim d.o.o. (Matjaž Mozetič)
#    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Work Breakdown Structure',
    'version': '8.0.3.0.0',
    'author': 'Matmoz d.o.o., '
              'Luxim d.o.o., '
              'Deneroteam, '
              'Eficent, '
              'Project Expert Team',
    'contributors': [
        'Jordi Ballester <jordi.ballester@eficent.com>',
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
        'Vijaykumar Baladaniya <vijay@deneroteam.com>'
    ],
    'website': 'http://project.expert',
    'category': 'Advanced Project Management',
    'license': 'AGPL-3',
    'depends': [
        'project',
        'analytic',
        'project_issue',
        'account_analytic_analysis',
        'web_one2many_kanban'
    ],
    'summary': 'Project Work Breakdown Structure',
    'data': [
        'views/account_analytic_account_view.xml',
        'views/project_project_view.xml',
        'data/category_data.xml'
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'application': True,
}
