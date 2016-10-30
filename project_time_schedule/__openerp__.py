# -*- coding: utf-8 -*-
{
    'name': 'Project Time Management - Activity Scheduling',
    'version': '8.0.1.0.2',
    'author':   'Eficent, '
                'Matmoz d.o.o., '
                'Project Expert Team',
    'contributors': [
        'Jordi Ballester <jordi.ballester@eficent.com>',
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'summary': 'Activity Scheduling',
    'depends': [
        'project',
    ],
    'data': [
        'views/project_time_schedule_view.xml',
        'wizard/project_task_calculate_network.xml'
    ],
    'test': [
    ],
    'installable': True,
    'active': False,
    'certificate': '',
}
