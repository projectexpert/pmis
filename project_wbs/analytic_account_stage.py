# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#               <contact@eficent.com>
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

from openerp import tools
from openerp.osv import fields, osv
from openerp.tools.translate import _

_ANALYTIC_ACCOUNT_STATE = [('draft', 'New'),
                           ('open', 'In Progress'),
                           ('pending', 'To Renew'),
                           ('close', 'Closed'),
                           ('cancelled', 'Cancelled')]


class analytic_account_stage(osv.osv):
    _name = 'analytic.account.stage'
    _description = 'Analytic Account Stage'
    _order = 'sequence'
    _columns = {
        'name': fields.char('Stage Name', required=True, size=64, translate=True),
        'description': fields.text('Description'),
        'sequence': fields.integer('Sequence'),
        'analytic_account_ids': fields.many2many('account.analytic.account', 'analytic_account_stage_rel', 'stage_id', 'analytic_account_id', 'Project/Analytic stages'),
        'fold': fields.boolean('Folded by Default',
                               help="This stage is not visible, "
                                    "for example in status bar or kanban view, "
                                    "when there are no records in that stage to display."),
        'case_default': fields.boolean('Default for New Projects',
                                       help="If you check this field, this stage will be proposed "
                                            "by default on each new project. "
                                            "It will not assign this stage to existing projects."),
    }

    def _get_default_parent_id(self, cr, uid, ctx={}):
        analytic = ctx.get('default_parent_id', False)
        if type(analytic) is int:
            return [analytic]
        return analytic

    _defaults = {
        'sequence': 1,
        'fold': False,
        'case_default': False,
        'analytic_account_ids': _get_default_parent_id,
    }

    _order = 'sequence'

    def copy(self, cr, uid, id, default=None, context=None):
        if context is None:
            context = {}
        if default is None:
            default = {}

        default['analytic_account_ids'] = []
        res = super(analytic_account_stage, self).copy(cr, uid, id, default, context)
        return res

analytic_account_stage()
