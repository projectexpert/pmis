# -*- coding: utf-8 -*-
{
    'name': 'Project Issue to Change Request',
    'version': '8.0.1.0.3',
    'summary': 'Create Change Requests from Project Issues',
    'sequence': '19',
    'complexity': 'easy',
    'author':   'Matmoz d.o.o., '
                'Project Expert Team',
    'contributors': [
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'data': [
        'views/change_request_view.xml'
    ],
    'depends': ['project_issue', 'change_management'],
    'installable': True,
}
