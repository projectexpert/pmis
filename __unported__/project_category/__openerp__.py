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
    "name": "Project Categorization",
    "version": "1.0",
    "author": "Eficent",
    "website": "http://www.eficent.com",
    "category": "Generic Modules/Projects & Services",
    "depends": [
                "base",
                "project",                       
                ],
    "description": """ This module introduces the possibility to associate categories to analytic accounts and projects.
        Manage the analytic account categories in order to better classify them for tracking and analysis purposes. 
        An analytic account may belong to several categories and categories have a hierarchy structure: an analytic account belonging to a category also belong to her parent category.
    """,
    "init_xml": [
                ],
    "update_xml": [    
        "analytic_account_category.xml",
        "analytic_account_view.xml",
        "project_view.xml",
        "security/ir.model.access.csv",
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
