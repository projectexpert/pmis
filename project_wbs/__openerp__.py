# -*- coding: utf-8 -*-
{
    'name': 'Work Breakdown Structure',
    'version': '8.0.2.4.5',
    'author': 'Eficent, '
              'Matmoz, '
              'Luxim, '
              'Project Expert Team',
    'contributors': [
        'Jordi Ballester <jordi.ballester@eficent.com>',
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'website': 'http://project.expert',
    'category': 'Project Management',
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
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'application': True,
}
