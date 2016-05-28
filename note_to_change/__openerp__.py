# coding: utf-8

{
    'name': 'Convert Note to CR',
    'version': '8.0.1.0.0',
    'author':   'Matmoz d.o.o., '
                'Project Expert Team',
    'contributors': [
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'summary': '''Convert a note to a Change Request''',
    'depends': [
        'base',
        'note',
        'change_management'
    ],
    'demo': [],
    'data': [
        'wizard/convert_note_view.xml',
        'view/note_view.xml'
    ],
    'test': [],
    'js': [],
    'css': [],
    'qweb': [],
    'installable': True,
    'auto_install': False,
}
