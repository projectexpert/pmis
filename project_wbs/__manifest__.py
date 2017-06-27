# -*- coding: utf-8 -*-
{
    'name': 'Work Breakdown Structure',
    'version': '9.0.1.0.0',
    'author': 'Deneroteam. <dhaval@deneroteam.com>',
    'website': 'http://deneroteam.com/',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'depends': [
        'project',
        'account',
        'analytic',
        'account_analytic_parent',
        'project_issue',
        # 'project_timesheet',
        'web_one2many_kanban'
    ],
    'summary': 'Project Work Breakdown Structure',
    'data': [
        'data/data.xml',
        'view/account_analytic_account_view.xml',
        'view/project_project_view.xml',
        # 'view/project_configuration.xml',
    ],
    'css': [
        'static/src/css/project_kanban.css',
    ],
    'installable': False,
    'application': True,
}
