# -*- coding: utf-8 -*-
# Copyright 2014-17 Eficent Business and IT Consulting Services S.L.
#        <contact@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Project progress measurement",
    "version": "10.0.1.0.0",
    "author": "Eficent, "
              "Project Expert Team",
    "website": "http://project.expert",
    "category": "Project Management",
    "license": "AGPL-3",
    "depends": [
        "project",
        "progress_measurement",
        "project_wbs"
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/progress_measurements_entry_view.xml",
        "views/project_progress_measurement_view.xml",
        "views/project_project_view.xml",
    ],
    "installable": True,
    "application": True,
}
