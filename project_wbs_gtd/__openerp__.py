# -*- coding: utf-8 -*-

{
    'name': 'Project Level Todo',
    'version': '8.0.2.0.1',
    'author': 'OpenERP SA, '
              'Matmoz d.o.o., '
              'Project Expert Team',
    'contributors': [
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'summary': '''GTD View on Project WBS Level''',
    'depends': ['project', 'project_gtd', 'project_wbs'],
    'data': [
        'project_gtd_data.xml',
        'project_gtd_view.xml',
        'security/ir.model.access.csv',
    ],
    'demo': ['project_gtd_demo.xml'],
    'installable': True,
    'auto_install': False,
}
