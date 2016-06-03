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
        cr, uid, context = self.env.args
        context = dict(context)
        # Find the previous stage
        res = super(AccountAnalyticAccount, self).write(values)
        if values.get('stage_id'):
            project_obj = self.env['project.project']
            stage_obj = self.env['analytic.account.stage']
            for acc in self:
                # Search if there's an associated project
                project = project_obj.search(
                    [('analytic_account_id', '=', acc.id)]
                )

                stage = stage_obj.browse(values.get('stage_id'))
                cr, uid, context = self.env.args

                if stage.project_state == 'close':
                    project.set_done()
                elif stage.project_state == 'cancelled':
                    project.set_cancel()
                elif stage.project_state == 'pending':
                    project.set_pending()

                # This part is commented, beacuse the progress state can belong
                # to several stages, thus by this line we would skip to the
                # last stage if there were more than one stages related to
                # this state (in progress)
                #
                # elif stage.project_state == 'open':
                #     project.set_open()
        return res
