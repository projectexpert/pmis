# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Avangard Enterprise Information Systems (<http://www.avangard-eis.com/>)
#              Jordi Ballester <jordi.ballester@avangard-eis.com>
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
    "name": "Project Management",
    "version": "1.0",
    "author": "Jordi Ballester (Eficent)",
    "website": "http://www.eficent.com",
    "category": "Generic Modules/Projects & Services",
    "depends": ["account", "analytic", "product", "project", "purchase_requisition", "purchase"],
    "description": """
        This module adds the possibility to create and link purchase requisitions and purchase orders to a project.
        - The project form adds a tab 'Purchase' containing the purchase requisitions and orders for this project.
        - There's a link from the project form to the related purchase requisitions and purchase orders in a separate view.
        - In the purchase views it is possible to filter by project, and the project is displayed in the list and form views.

    """,
    "init_xml": [
                ],
    "update_xml": [            
        "purchase_order_view.xml",
        "purchase_requisition_view.xml",
        "project_view.xml",     
        "security/ir.model.access.csv",
        "security/project_procurement_security.xml",
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
