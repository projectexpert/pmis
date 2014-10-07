# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
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
    "name": "Analytic Resource Planning",
    "version": "1.0",
    "author": "Eficent",
    "website": "www.eficent.com",
    "category": "Generic Modules/Projects & Services",
    "depends": ["account", "purchase", "analytic_plan"],
    "description": """
Analytic Resource Planning
====================================
    An effective planning of the resources required for a project or analytic account
    becomes essential in organizations that are run by projects, or profit center accounting.
    The process of resource planning generally follows an rolling wave planning approach, in which
    the level of detail of the planned resources increases over time, as the details of the work required
    are known to the planning group.

    Resources planned for a project/analytic account have an impact on the planned costs.
    If the resources are procured internally, the standard cost is determined.
    If the resources are procured externally, the user can indicate the supplier, and the planned costs
    are then determined on the basis of the supplier's price list.

    Multiple planning versions can be maintained for a resource plan, so that the organization can create
    a first rough-cut resource plan, that can then be refined as the project progresses.

    """,
    "init_xml": [],
    "update_xml": [
        "analytic_resource_plan_view.xml",
        "analytic_account_view.xml",
        "product_view.xml",
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
