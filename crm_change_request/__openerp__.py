{
    'name': 'Lead to Change Request',
    'version': '1.0',
    'summary': 'Create Change Requests from Leads',
    'sequence': '19',
    'category': 'Project Management',
    'complexity': 'easy',
    'author': 'Matmoz d.o.o.',
    'description': """
Lead to Change Requests
=======================

Link module to map leads to change requests
        """,
    'data': [
        'change_request_view.xml'
    ],
    'depends': ['crm', 'change_management'],
    'installable': True,
}
