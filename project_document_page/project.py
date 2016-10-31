# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010 (Original Author)
#    Domsense s.r.l. (<http://www.domsense.com>)
#
#    Copyright (C) 2014-now (OpenERP version 7 adaptation)
#    Matmoz d.o.o. (<http://www.matmoz.si>)
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
from openerp import models, fields


class Project(models.Model):
    _inherit = 'project.project'

    page_ids = fields.Many2many(
        'document.page',
        'project_docu_rel',
        'project_id',
        'page_id',
        'Document pages'
    )


class Project(models.Model):
    _inherit = 'project.task'

    page_ids = fields.Many2many(
        'document.page',
        'task_page_rel',
        'task_id',
        'page_id',
        'Document pages'
    )
