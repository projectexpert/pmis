# -*- coding: utf-8 -*-
# © 2015 MATMOZ d.o.o. - Matjaž Mozetič
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields, osv
from openerp import tools


class WbsGtdContext(osv.Model):

    _name = "wbs.gtd.context"
    _description = "Context"
    _columns = {
        'name': fields.char(
            'Context', size=64, required=True, translate=True),
        'sequence': fields.integer(
            'Sequence',
            help=("Gives the sequence order when displaying "
                  "a list of contexts.")),
    }
    _defaults = {
        'sequence': 1
    }
    _order = "sequence, name"


class WbsGtdTimebox(osv.Model):

    _name = "wbs.gtd.timebox"
    _order = "sequence"
    _columns = {
        'name': fields.char(
            'Timebox', size=64, required=True, select=1, translate=1),
        'sequence': fields.integer(
            'Sequence',
            help="Gives the sequence order when displaying "
                 "a list of timebox."),
    }


class WbsWorkpackage(osv.Model):

    _inherit = "project.project"
    _columns = {
        'wbstimebox_id': fields.many2one(
            'wbs.gtd.timebox',
            "Timebox",
            help="Time-laps during which the workpackage has to be treated"),
        'wbscontext_id': fields.many2one(
            'wbs.gtd.context',
            "Context",
            help="The context place where user has to treat the workpackage"),
    }

    def _get_wbscontext(self, cr, uid, context=None):
        ids = self.pool.get('wbs.gtd.context').search(
            cr, uid, [], context=context)
        return ids and ids[0] or False

    def _read_group_wbstimebox_ids(
            self, cr, uid, ids, domain,
            read_group_order=None, access_rights_uid=None, context=None):
        """Used to display all timeboxes on the view."""
        wbstimebox_obj = self.pool.get('wbs.gtd.timebox')
        order = wbstimebox_obj._order
        access_rights_uid = access_rights_uid or uid
        wbstimebox_ids = wbstimebox_obj._search(
            cr, uid, [],
            order=order, access_rights_uid=access_rights_uid, context=context)
        result = wbstimebox_obj.name_get(
            cr, access_rights_uid, wbstimebox_ids, context=context)
        # Restore order of the search
        result.sort(
            lambda x, y: cmp(
                wbstimebox_ids.index(x[0]), wbstimebox_ids.index(y[0])
            )
        )
        fold = dict.fromkeys(wbstimebox_ids, False)
        return result, fold

    def _read_group_stage_ids(
            self, cr, uid, ids, domain,
            read_group_order=None, access_rights_uid=None,
            context=None
    ):
        stage_obj = self.pool.get('analytic.account.stage')
        order = stage_obj._order
        access_rights_uid = access_rights_uid or uid
        if read_group_order == 'stage_id desc':
            order = '%s desc' % order
        search_domain = []
        analytic_account_id = self._resolve_analytic_account_id_from_context(
            cr, uid, context=context
        )
        if analytic_account_id:
            search_domain += [
                '|', ('analytic_account_ids', '=', analytic_account_id)
            ]
        search_domain += [('id', 'in', ids)]
        stage_ids = stage_obj._search(
            cr, uid, [], order=order,
            access_rights_uid=access_rights_uid,
            context=context
        )
        result = stage_obj.name_get(
            cr, access_rights_uid, stage_ids,
            context=context
        )
        # restore order of the search
        result.sort(
            lambda x, y: cmp(
                stage_ids.index(x[0]),
                stage_ids.index(y[0])
            )
        )

        fold = {}
        for stage in stage_obj.browse(
            cr, access_rights_uid, stage_ids,
            context=context
        ):
            fold[stage.id] = stage.fold or False
        return result, fold

    _defaults = {
        'wbscontext_id': _get_wbscontext
    }

    _group_by_full = {
        'wbstimebox_id': _read_group_wbstimebox_ids,
        'stage_id': _read_group_stage_ids,
    }

# CORRECT THE ORIGINAL PROJECT_GTD (TASK LEVEL) BEHAVIOUR ON FOLDED KANBAN

class ProjectTask(osv.Model):
    _inherit = "project.task"

    def _get_context(self, cr, uid, context=None):
        ids = self.pool.get('project.gtd.context').search(
            cr, uid, [], context=context)
        return ids and ids[0] or False

    def _read_group_timebox_ids(
            self, cr, uid, ids, domain,
            read_group_order=None, access_rights_uid=None, context=None):
        """Used to display all timeboxes on the view."""
        timebox_obj = self.pool.get('project.gtd.timebox')
        order = timebox_obj._order
        access_rights_uid = access_rights_uid or uid
        timebox_ids = timebox_obj._search(
            cr, uid, [],
            order=order, access_rights_uid=access_rights_uid, context=context)
        result = timebox_obj.name_get(
            cr, access_rights_uid, timebox_ids, context=context)
        # Restore order of the search
        result.sort(
            lambda x, y: cmp(timebox_ids.index(x[0]), timebox_ids.index(y[0])))
        fold = dict.fromkeys(timebox_ids, False)
        return result, fold

    def _read_group_stage_ids(
            self, cr, uid, ids, domain,
            read_group_order=None, access_rights_uid=None, context=None
    ):
        stage_obj = self.pool.get('project.task.type')
        order = stage_obj._order
        access_rights_uid = access_rights_uid or uid
        if read_group_order == 'stage_id desc':
            order = '%s desc' % order
        search_domain = []
        project_id = self._resolve_project_id_from_context(
            cr, uid, context=context
        )
        if project_id:
            search_domain += ['|', ('project_ids', '=', project_id)]
        search_domain += [('id', 'in', ids)]
        stage_ids = stage_obj._search(
            cr, uid, [], order=order,
            access_rights_uid=access_rights_uid, context=context
        )
        result = stage_obj.name_get(
            cr, access_rights_uid, stage_ids, context=context
        )
        # restore order of the search
        result.sort(
            lambda x, y: cmp(stage_ids.index(x[0]), stage_ids.index(y[0]))
        )

        fold = {}
        for stage in stage_obj.browse(
                cr, access_rights_uid, stage_ids, context=context
        ):
            fold[stage.id] = stage.fold or False
        return result, fold

    _defaults = {
        'context_id': _get_context
    }

    _group_by_full = {
        'timebox_id': _read_group_timebox_ids,
        'stage_id': _read_group_stage_ids,
    }
