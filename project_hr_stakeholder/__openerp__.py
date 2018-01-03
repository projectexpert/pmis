# -*- coding: utf-8 -*-

{
    'name': 'Project Stakeholder Management',
    'version': '8.0.2.0.9',
    'author': 'Eficent, '
              'Matmoz d.o.o., '
              'Project Expert Team',
    'contributors': [
        'Jordi Ballester <jordi.ballester@eficent.com>',
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'website': 'http://project.expert',
    'category': 'Advanced Project Management',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'project',
        'analytic_plan',
        'project_charter'
    ],
    'data': [
        'project_hr_role.xml',
        'project_hr_responsibility.xml',
        'project_hr_stakeholder.xml',
        'project_view.xml',
        'security/ir.model.access.csv',
        'security/project_security.xml',
        'project_hr_stakeholder_data.xml',
    ],
    'demo': [

    ],
    'test': [
    ],
    'installable': True,
    'active': False,
    'certificate': '',
}
