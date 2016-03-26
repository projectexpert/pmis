# -*- coding: utf-8 -*-
#    Copyright (C) 2015 Matmoz d.o.o. (Matjaž Mozetič)
#    Copyright (C) 2015 Eficent (Jordi Ballester Alomar)
#    Copyright (C) 2015 Serpent Consulting Services (Sudhir Arya)
#    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, models
from openerp.tools import misc


class Project(models.Model):
    _inherit = "project.project"
    _description = "WBS Element"

    @api.multi
    def write(self, values):
        cr, uid, context = self.env.args
        context = dict(context)
        for p in self:
            if values.get('state') and (
                not values.get('stage_id') and not
                context.get('stage_updated')
            ):
                if not context.get('change_project_stage_from_status'):
                    context.update(
                        {'change_project_stage_from_status': True}
                    )
                    self.env.args = cr, uid, misc.frozendict(context)
                    # Change the stage corresponding to the new status
                    if p.parent_id and p.parent_id.child_stage_ids:
                        for stage in p.parent_id.child_stage_ids:
                            if stage.project_state == values.get('state'):
                                values.update({'stage_id': stage.id})
        return super(Project, self).write(values)


class AccountAnalyticAccount(models.Model):

    _inherit = 'account.analytic.account'

    @api.multi
    def write(self, values):
        # Find the previous stage
        old_stage_id = {}
        old_state_id = {}
        for acc in self:
            old_stage_id[acc.id] = acc.stage_id or False
            old_state_id[acc.id] = acc.state
        res = super(AccountAnalyticAccount, self).write(values)
        if values.get('stage_id'):
            project_obj = self.env['project.project']
            stage_obj = self.env['analytic.account.stage']
            for acc in self:
                # Search if there's an associated project
                project = project_obj.search(
                    [('analytic_account_id', '=', acc.id)]
                )
                if old_stage_id[acc.id]:
                    old_stage = acc.stage_id
                else:
                    old_stage = False
                new_stage = stage_obj.browse(values.get('stage_id'))
                cr, uid, context = self.env.args
                context = dict(context)
                context.update({
                    'stage_updated': True
                })
                # If the new stage is found in the child accounts, then set
                # it as well (only if the new stage sequence is greater than
                #  the current)
                if new_stage.id in [st.id for st in acc.child_stage_ids]:
                    child = self.search([('parent_id', '=', acc.id)])
                    if child.stage_id.sequence < new_stage.sequence:
                        child.with_context(context).write(
                            {'stage_id': new_stage.id}
                        )
                        self.env.args = cr, uid, misc.frozendict(context)
                if (
                    old_stage and
                    old_stage.project_state == new_stage.project_state
                ):
                    continue
                if new_stage.project_state == 'close':
                    project.set_done()
                elif new_stage.project_state == 'cancelled':
                    project.set_cancel()
                elif new_stage.project_state == 'pending':
                    project.set_pending()
                elif new_stage.project_state == 'open':
                    project.set_open()
        return res
