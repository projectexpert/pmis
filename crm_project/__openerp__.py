# -*- coding: utf-8 -*-
# © 2015 MATMOZ d.o.o.. <info@matmoz.si>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'CRM cases part of Projects',
    'version': '8.0.0.8.4',
    'author':   'Matmoz d.o.o., '
                'Project Expert Team',
    'contributors': [
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'summary': '''CRM tasks and CRM leads connected to project''',
    'depends': ['crm', 'project_charter', 'project_issue'],
    'data': [
        'views/crm_opportunity.xml',
        'views/project_lead.xml',
        'views/project_opportunity.xml',
        'views/leads_project_view.xml'
    ],
    'qweb': [],
    'demo': [],
    'test': [],
    'active': False,
    'installable': True
}
