# -*- coding: utf-8 -*-
{
    'name': 'Work Breakdown Structure',
    'version': '8.0.2.2.9',
    'author': 'Eficent, '
              'Matmoz d.o.o., '
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
        'account_analytic_analysis'
    ],
    'summary': 'Project Work Breakdown Structure',
    'data': [
        'view/account_analytic_account_view.xml',
        'view/project_project_view.xml',
        'view/project_configuration.xml',
        # 'security/ir.model.access.csv',
    ],
    'demo': [

    ],
    'test': [
    ],
    'installable': True,
    'application': True,
}
