# -*- coding: utf-8 -*-

{
    'name': 'Project Charter',
    'version': '8.0.1.2.3',
    'author': 'Matmoz d.o.o., '
              'Project Expert Team',
    'contributors': [
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'sequence': 9,
    'summary': 'Project Charter',
    'complexity': 'easy',
    'images': [],
    'depends': [
        'project',
        'analytic_account_sequence',
        'analytic_plan',
        'analytic_resource_plan',
        'analytic_billing_plan',
        'project_wbs',
        'web_ckeditor4',
    ],
    'data': ['views/project_charter_view.xml',
             'views/analytic_view.xml',
             'security/ir.model.access.csv'],
    'test': [],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
