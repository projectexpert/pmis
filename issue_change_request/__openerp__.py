{
    'name': 'Project Issue to Change Request',
    'version': '1.0',
    'summary': 'Create Change Requests from Project Issues',
    'sequence': '19',
    'category': 'Project Management',
    'complexity': 'easy',
    'author': 'Matmoz d.o.o.',
    'description': """
Issues to Change Requests
=========================

Link module to map issues to change requests
        """,
    'data': [
        'change_request_view.xml'
    ],
    'depends': ['project_issue', 'change_management'],
    'installable': True,
}
