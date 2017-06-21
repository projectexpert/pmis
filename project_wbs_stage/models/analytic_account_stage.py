# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Luxim d.o.o.
# Copyright 2017 Matmoz d.o.o.
# Copyright 2017 Deneroteam.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models

_ANALYTIC_ACCOUNT_STATE = [('draft', 'New'),
                           ('open', 'In Progress'),
                           ('pending', 'To Renew'),
                           ('close', 'Closed'),
                           ('cancelled', 'Cancelled')]


class AnalyticAccountStage(models.Model):
    _name = 'analytic.account.stage'
    _description = 'Analytic Account Stage'
    _order = 'sequence'

    @api.model
    def _get_default_parent_id(self):
        analytic = self.env.context.get('default_parent_id', False)
        if type(analytic) is int:
            return [analytic]
        return analytic


    name = fields.Char('Stage Name', required=True, size=64, translate=True)
    description = fields.Text('Description')
    sequence = fields.Integer('Sequence', default=1)
    analytic_account_ids = fields.Many2many(
        'account.analytic.account', 'analytic_account_stage_rel', 'stage_id',
        'analytic_account_id', 'Project/Analytic stages',
        default=_get_default_parent_id, copy=False)
    fold = fields.Boolean(
        'Folded by Default',
        help="This stage is not visible, for example in status bar or kanban "
             "view, when there are no records in that stage to display.",
        default=False)
    case_default = fields.Boolean(
        'Default for New Projects',
        help="If you check this field, this stage will be proposed by default "
             "on each new project. It will not assign this stage to existing "
             "projects.", default=False)
    project_state = fields.Selection(
        [('open', 'In Progress'), ('cancelled', 'Cancelled'),
         ('pending', 'Pending'), ('close', 'Closed')], 'Project Status',
        required=True)
