# -*- coding: utf-8 -*-
{
    'name': 'Project Meetings',
    'version': '8.0.1.0.0',
    'summary': 'Meetings in project communications tab',
    'author':   'Matmoz d.o.o., '
                'Project Expert Team',
    'contributors': [
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'depends': ['calendar', 'project_charter'],
    'data': [
        'views/project_view.xml',
        'views/meeting_view.xml',
    ],
    'demo': [],
    'installable': True,
}
