# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Eficent (<http://www.eficent.com/>)
#              <contact@eficent.com>
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
    "name": "Project Milestone Management",
    "version": "1.0",
    "author": "Eficent",
    "website": "www.eficent.com",
    "category": "Generic Modules/Projects & Services",
    "depends": ["project"],
    "description": """
    
    == Classify tasks as milestones  ==
    Eficent brings you this module to classify tasks as milestones.
    
    It is possible to introduce the Project Percentage of Completion and the invoice percentage for informative purposes.
    
    A separate entry is created in the menu to register milestones.
    
    The project form is extended to add a 'Milestones' tab.
                  
   == More information and assistance ==
   
   If you are interested in this module and seek further assistance to use it please visit us at www.eficent.com or conact us at contact@eficent.com
 
    """,
    "init_xml": [],
    "update_xml": [    
        "project_time_milestone_view.xml",        
    ],
    'demo_xml': [

    ],
    'test':[
    ],
    'installable': True,
    'active': False,
    'certificate': '',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
