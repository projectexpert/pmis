# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Luxim d.o.o.
# Copyright 2017 Matmoz d.o.o.
# Copyright 2017 Deneroteam.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models

class ProjectProject(models.Model):
    _name = "project.project"
    _inherit = "project.project"
    _description = "WBS element"


    @api.model
    def _resolve_analytic_account_id_from_context(self):
        """ Returns ID of parent analytic account based on the value of
        'default_parent_id'
            context key, or None if it cannot be resolved to a single
            account.analytic.account
        """
        if type(self.env.self.env.context.get('default_parent_id')) in (int, long):
            return context['default_parent_id']
        if isinstance(self.env.self.env.context.get('default_parent_id'), basestring):
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

    _group_by_full = {
        'stage_id': _read_group_stage_ids,
    }

    @api.multi
    def write(self, values):
        for p in self:
            if values.get('state', False) and \
                    (not values.get('stage_id', False) and not
                    self.env.context.get('stage_updated', False)):
                if not self.env.context.get(
                        'change_project_stage_from_status', False):
                    self = self.with_context.update(
                        change_project_stage_from_status=True)
                    # Change the stage corresponding to the new status
                    if p.parent_id and p.parent_id.child_stage_ids:
                        for stage in p.parent_id.child_stage_ids:
                            if stage.project_state == values.get('state'):
                                values.update({'stage_id': stage.id})
        return super(ProjectProject, self).write(values)
