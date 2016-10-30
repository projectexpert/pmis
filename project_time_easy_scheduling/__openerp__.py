# -*- coding: utf-8 -*-
{
    'name': 'Project Easy Scheduling tool',
    'version': '8.0.1.0.2',
    'author':   'Eficent, '
                'Project Expert Team',
    'contributors': [
        'Jordi Ballester <jordi.ballester@eficent.com>',
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'summary': 'Better project schedule by introducing an activities view',
    'depends': [
        'project_time_milestone',
        'project_time_schedule',
        'project_time_sequence',
        'project_wbs',
    ],
    'data': [
        'views/project_task_view.xml'
    ],
    'test': [
    ],
    'installable': True,
    'active': False,
    'certificate': '',
}
