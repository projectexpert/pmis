# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Enterprise Management Solution
#
#    Copyright (C) 2015 Matmoz d.o.o. (<http://www.matmoz.si>).
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
    "name": "Change Management",
    "version": "2.5",
    "author":   "Matmoz d.o.o.",
    "website":  "http://www.matmoz.si",
    "category": "Project Management",
    "license": "AGPL-3",
    "contributors": [
        "Matjaž Mozetič <m.mozetic@matmoz.si>",
    ],
    "summary": "Change Management integrated with Stakeholders Requirements",
    "depends": ["project", "project_charter", "project_hr_stakeholder"],
    "data": [
        "data/change_management_data.xml",
        "data/change_management_sequence.xml",
        "security/ir.model.access.csv",
        "view/project_task_view.xml",
        "view/change_management_view.xml",
        "view/change_management_category_view.xml",
        "view/change_management_proximity_view.xml",
        "view/change_management_menus.xml"
    ],
    "demo": ["demo/change_management_demo.xml"],
    "test": ["test/test_change_management.yml"],
    "license": "AGPL-3",
    "installable": True,
    "application": True,
    "active": False,
}
