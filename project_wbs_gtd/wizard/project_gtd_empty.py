# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp.osv import fields, osv
from openerp.tools.translate import _


class wbs_timebox_empty(osv.TransientModel):
    _name = 'wbs.timebox.empty'
    _description = 'Project Timebox Empty'
    _columns = {
        'name': fields.char('Name', size=32),
    }

    def view_init(self, cr, uid, fields_list, context=None):
        if context is None:
            context = {}
        self._empty(cr, uid, context=context)

    def _empty(self, cr, uid, context=None):
        close = []
        up = []
        obj_tb = self.pool.get('wbs.gtd.timebox')
        obj_wbs = self.pool.get('wbs.project')

        if context is None:
            context = {}
        if 'active_id' not in context:
            return {}

        ids = obj_tb.search(cr, uid, [], context=context)
        if not len(ids):
            raise osv.except_osv(
                _('Error!'), _('No timebox child of this one!'))
        wids = obj_wbs.search(
            cr, uid, [('timebox_id', '=', context['active_id'])])
        for project in obj_wbs.browse(cr, uid, wids, context):
            if (wbs.stage_id and wbs.stage_id.fold) \
                    or (project.user_id.id != uid):
                close.append(project.id)
            else:
                up.append(project.id)
        if up:
            obj_wbs.write(cr, uid, up, {'timebox_id': ids[0]})
        if close:
            obj_wbs.write(cr, uid, close, {'timebox_id': False})
        return {}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
