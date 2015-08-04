# -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Enterprise Management Solution
#    risk_management Module
#    Copyright (C) 2011 ValueDecision Ltd (<http://www.valuedecision.com>).
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
    'name': 'Risk Management',
    'version': '2.0',
    'author': 'Tactix4 Ltd',
    'website': 'http://www.tactix4.com',
    'category': 'Project Management',
    'description': """
       This module allows to manage risk in at least two different contexts:

       1) Project Management

       2) Business Continuity Planning
       
       A risk is always associated with a project and has an impact and probability assessment pre- and post-response with resulting expected values (scores).
       Actions on risk are tasks, which can be identified easily in the extended task view (Projects > Tasks) via the 'Action on Risk' filter and associated risk id.
       In addition, tasks which are actions on risks are coloured green in the task list (tree) view.
       
       Risk categories, response categories and proximity are set-up according to the PRINCE2 project methodology as well as for Business Continuity Planning.
       They are easily changed via the 'Configuration' menu to get them in accordance with PIP, SCRUM or DSDM.
       
       Besides the above mentioned information the following information can and ought to be documented as well:
       Risk description, author, date registered, date modified, event, effect, cause and risk owner.
       
       Two user groups are added, which a user must be associated with to work with Risks, either Risk / User or Risk / Manager.

       
    """,
    'depends': ['project'],
    'update_xml':['risk_management_data.xml',
                  'risk_management_sequence.xml',
                  'security/risk_management_security.xml',
                  'security/ir.model.access.csv',
                  'view/project_task_view.xml',
                  'view/risk_management_view.xml',
                  'view/risk_management_category_view.xml',
                  'view/risk_management_category_response_view.xml',
                  'view/risk_management_proximity_view.xml',
                  'view/risk_management_menus.xml'],
    'demo': ['risk_management_demo.xml'],
    'test': ['test/test_risk_management.yml'],
    'installable': True,
    'application': True,
    'active': False,
}

