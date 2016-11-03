# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Analytic account code sequence',
    'summary': 'Analytic account code sequence',
    'version': '8.0.1.0.2',
    'author':   'Eficent, '
                'SerpentCS ,'
                'Project Expert Team',
    'contributors': [
        'Jordi Ballester <jordi.ballester@eficent.com>',
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
        'Sudhir Arya <http://www.serpentcs.com/>'
    ],
    'website': 'http://project.expert',
    'category': 'Project Management',
    'depends': ['project_wbs'],
    'data': [
        'views/analytic_account_sequence_view.xml',
        'data/analytic_account_sequence_data.xml',
        'views/account_analytic_account_view.xml',
        'security/ir.model.access.csv',
    ],
    'test': [
    ],
    'installable': True,
    'active': False,
    'certificate': '',
    'application': True,
    'license': 'AGPL-3',
}
