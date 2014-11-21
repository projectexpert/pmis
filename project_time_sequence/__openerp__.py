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
    "name": "Project activity sequencing",
    "version": "1.0",
    "author": "Eficent",
    "website": "",
    "category": "Generic Modules/Projects & Services",
    "depends": ["project"],
    "description": """
     
 == Sequence the activities of your projects ==
    Eficent brings you this module to better manage the activity sequencing within your projects.
  
    The aim is to enable the department responsible for projects to identify the relationship between activities (tasks and milestones) of the project.
   
                 
   == More information and assistance ==
   
   If you are interested in this module and seek further assistance to use it please visit us at www.eficent.com or conact us at contact@eficent.com
 
         
  

    """,
    "init_xml": [
                ],
    "update_xml": [    
        "wizard/project_task_link_predecessors.xml",
        "project_time_sequence_view.xml",
        
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
