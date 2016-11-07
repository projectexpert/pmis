# -*- coding: utf-8 -*-
# © 2015 MATMOZ d.o.o.. <info@matmoz.si>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


{
    'name': 'Tasks on CRM',
    'version': '8.0.1.0.5',
    'author':   'Matmoz d.o.o., '
                'Project Expert Team',
    'contributors': [
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'summary': '''Todo list for CRM leads and opportunities''',
    'depends': ['crm_project', 'project_gtd'],
    'data': [
        'views/crm_todo_view.xml',
        'views/crm_todo_opportunity.xml',
        'views/crm_todo_project_task_tree.xml'
    ],
    'demo': ['crm_todo_demo.xml'],
    'installable': True,
    'auto_install': False,
}
