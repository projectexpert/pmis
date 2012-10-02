# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Eficent (<http://www.eficent.com/>)
#              Jordi Ballester Alomar <jordi.ballester@eficent.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    'name': 'Project Mailgate Note for Projects',
    'version': '1.0',
    'category': 'Generic Modules/Projects & Services',
    'description': """This module allows to add a note or send an email from the history tab in the project form view.""",
    "author": "Jordi Ballester (Eficent)",
    "website": "http://www.eficent.com",
    'depends': [
        'base',
        'crm',
        'project_communications_mailgate',
    ],
    'init_xml': [],
    'images': [
        'images/accueil.png',
        'images/send_mail.png',
        'images/history.png',
    ],
    'update_xml': [
        #'security/ir.model.access.csv',
        #'wizard/wizard.xml',
        'wizard/project_communications_add_note_view.xml',
        'wizard/project_communications_send_email_view.xml',
        'project_communications_mailgate_note_view.xml',
    ],
    'demo_xml': [],
    'test': [],
    #'external_dependancies': {'python': ['kombu'], 'bin': ['which']},
    'installable': True,
    'active': False,
    'license': 'AGPL-3',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
