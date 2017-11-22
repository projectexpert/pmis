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
import time
from openerp.osv import fields, osv
from openerp.tools.translate import _


class project_progress_measurement(osv.osv):

    _name = 'project.progress.measurement'
    _description = 'Project Progress Measurement'
    _inherit = "progress.measurement"
    _columns = {
        'project_id': fields.many2one('project.project', 'Project',
                                      ondelete='cascade',
                                      select="1",
                                      required=True),
    }

    _sql_constraints = [
        ('project_meas_type_date_uniq', 'unique(project_id, progress_measurement_type, communication_date)',
         _("Only one measurement of the same type can exist for each project on a given date."))
    ]

project_progress_measurement()
