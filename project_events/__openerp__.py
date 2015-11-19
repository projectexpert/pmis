# -*- encoding: utf-8 -*-
{
    "name": "Events in Projects",
    "version": "8.0.1.0.1",
    "depends": [
        "project_charter",
        "event",
    ],
    'summary': 'Events in project communications tab',
    'author':   'Matmoz d.o.o., '
                'Avanzosc, S.L., '
                'Project Expert Team',
    'contributors': [
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    "data": [
        "data/event_data.xml",
        "views/event_view.xml",
        "views/project_view.xml",
        "wizard/create_meeting_from_task_view.xml",
    ],
    "installable": True,
    "auto_install": False,
}
