# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Luxim d.o.o.
# Copyright 2017 Matmoz d.o.o.
# Copyright 2017 Deneroteam.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class AccountAnalyticAccount(models.Model):
    
    _inherit = 'account.analytic.account'

    @api.model
    def _resolve_analytic_account_id_from_context(self):
        """ Returns ID of parent analytic account based on the value of
        'default_parent_id'
            context key, or None if it cannot be resolved to a single
            account.analytic.account
        """
        if type(self.env.context.get('default_parent_id')) in (int, long):
            return context['default_parent_id']
        if isinstance(self.env.context.get('default_parent_id'), basestring):
            analytic_account_name = self.env.context['default_parent_id']
            analytic_account_ids = \
                self.env('account.analytic.account').name_search(
                    name=analytic_account_name)
            if len(analytic_account_ids) == 1:
                return analytic_account_ids[0][0]
        return None

    @api.model
    def _read_group_stage_ids(self, ids, domain, **kwargs):
        stage_obj = self.env['analytic.account.stage']
        order = stage_obj._order
        if read_group_order == 'stage_id desc':
            order = '%s desc' % order
        search_domain = []
        analytic_account_id = self._resolve_analytic_account_id_from_context()
        if analytic_account_id:
            search_domain += ['|', ('analytic_account_ids', '=',
                                    analytic_account_id)]
        search_domain += [('id', 'in', ids)]
        stage_ids = stage_obj._search(search_domain, order=order)
        result = stage_obj.name_get(stage_ids)
        # restore order of the search
        result.sort(lambda x, y: cmp(stage_ids.index(x[0]),
                                     stage_ids.index(y[0])))

        fold = {}
        for stage in stage_ids:
            fold[stage.id] = stage.fold or False
        return result, fold

    @api.model
    def _get_type_common(self):
        stages = self.env['analytic.account.stage'].search(
            [('case_default', '=', 1)])
        return stages

    stage_id = fields.Many2one(
        'analytic.account.stage', 'Stage',
        domain="['&', ('fold', '=', False), "
               "('analytic_account_ids', '=', parent_id)]")

    child_stage_ids = fields.Many2many(
        'analytic.account.stage', 'analytic_account_stage_rel',
        'analytic_account_id', 'stage_id', 'Child Stages', states={
            'close': [('readonly', True)], 'cancelled': [('readonly',
                                                          True)]},
        default=_get_type_common)

    _group_by_full = {
        'stage_id': _read_group_stage_ids,
    }

    @api.multi
    def write(self, values):
        # Find the previous stage
        old_stage_id = {}
        for acc in self:
            old_stage_id[acc.id] = acc.stage_id and acc.stage_id.id or False

        res = super(AccountAnalyticAccount, self).write(values)

        if values.get('stage_id'):
            project_obj = self.pool.get('project.project')
            stage_obj = self.pool.get('analytic.account.stage')
            for acc in self:
                # Search if there's an associated project
                project_ids = project_obj.search(
                    [('analytic_account_id', '=', acc.id)])
                if old_stage_id[acc.id]:
                    old_stage = stage_obj.browse(old_stage_id[acc.id])
                else:
                    old_stage = False
                new_stage = stage_obj.browse(values.get('stage_id'))
                self = self.with_context(stage_updated=True)
                # If the new stage is found in the child accounts, then set
                # it as well (only if the new stage sequence is greater than
                #  the current)
                if new_stage.id in [st.id for st in acc.child_stage_ids]:
                    child_ids = self.search(cr, uid,
                                            [('parent_id', '=', acc.id)])
                    for child in self.browse(cr, uid, child_ids,
                                             context=context):
                        if child.stage_id.sequence < new_stage.sequence:
                            child.write({'stage_id': new_stage.id})
                if old_stage and old_stage.project_state == \
                        new_stage.project_state:
                    continue
                if new_stage.project_state == 'close':
                    project_obj.set_done(project_ids)
                elif new_stage.project_state == 'cancelled':
                    project_obj.set_cancel(project_ids)
                elif new_stage.project_state == 'pending':
                    project_obj.set_pending(project_ids)
                elif new_stage.project_state == 'open':
                    project_obj.set_open(project_ids)
        return res
