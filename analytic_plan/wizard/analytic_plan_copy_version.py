# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# (Jordi Ballester Alomar)
#
# © 2015 Serpent Consulting Services Pvt. Ltd.
# (Sudhir Arya)
#
# © 2016 Matmoz d.o.o.
# (Matjaž Mozetič)
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models
from openerp.tools.translate import _
from openerp.exceptions import Warning as UserError


class AnalyticPlanCopyVersion(models.TransientModel):
    """
    For copying all the planned costs to a separate planning version
    """
    _name = "analytic.plan.copy.version"
    _description = "Analytic Plan copy versions"

    source_version_id = fields.Many2one(
        'account.analytic.plan.version',
        'Source Planning Version',
        required=True
    )
    dest_version_id = fields.Many2one(
        'account.analytic.plan.version',
        'Destination Planning Version',
        required=True
    )
    include_child = fields.Boolean(
        'Include child accounts',
        default=True
    )

    @api.multi
    def analytic_plan_copy_version_open_window(self):
        new_line_plan_ids = []
        analytic_obj = self.env['account.analytic.account']
        line_plan_obj = self.env['account.analytic.line.plan']

        data = self[0]
        record_ids = self._context and self._context.get('active_ids', False)
        active_model = self._context and self._context.get(
            'active_model', False
        )
        assert active_model == (
            'account.analytic.account', 'Bad context propagation'
        )
        record = analytic_obj.browse(record_ids)
        include_child = (
            data.include_child if data and data.include_child else False
        )
        source_version = (
            data.source_version_id if data and data.source_version_id else False
        )
        dest_version = (
            data.dest_version_id if data and data.dest_version_id else False
        )
        if dest_version.default_plan:
            raise UserError(
                _(
                    'It is prohibited to copy '
                    'to the default planning version.'
                )
            )
        if source_version == dest_version:
            raise UserError(
                _(
                    'Choose different source and destination '
                    'planning versions.'
                )
            )
        if include_child:
            account_ids = record.get_child_accounts().keys()
        else:
            account_ids = record_ids

        line_plans = line_plan_obj.search(
            [
                ('account_id', 'in', account_ids),
                ('version_id', '=', source_version.id)
            ]
        )
        new_line_plan_rec = line_plan_obj
        for line_plan in line_plans:
            new_line_plan = line_plan.copy()
            new_line_plan_rec += new_line_plan
            new_line_plan_ids.append(new_line_plan.id)
        if new_line_plan_rec:
            new_line_plan_rec.write({'version_id': dest_version[0]})

        return {
                'domain': "[('id','in', [" + ','.join(
                    map(str, new_line_plan_ids)
                ) + "])]",
                'name': _('Analytic Planning Lines'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.analytic.line.plan',
                'view_id': False,
                'context': False,
                'type': 'ir.actions.act_window'
        }
