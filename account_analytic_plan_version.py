# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#              <contact@eficent.com>
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
from openerp.tools.translate import _
from openerp.osv import fields, osv


class account_analytic_plan_version(osv.osv):
    _name = 'account.analytic.plan.version'
    _description = 'Analytic Planning Version'
    _columns = {
        'name': fields.char('Planning Version Name', size=64, required=True),
        'code': fields.char('Planning Version Code', size=8),
        'active': fields.boolean('Active',
                                 help='If the active '
                                      'field is set to False, '
                                      'it will allow you to hide '
                                      'the analytic planning version '
                                      'without removing it.'),
        'notes': fields.text('Notes'),
        'company_id': fields.many2one('res.company', 'Company', required=True),
        'default_committed': fields.boolean("""Default version
         for committed costs"""),
        'default_plan': fields.boolean('Default planning version'),
    }

    def _check_default_committed(self, cr, uid, vals, context=None):

        if 'default_committed' in vals:
            if vals['default_committed'] is True:
                other_default_committed = self.search(cr, uid, [('default_committed', '=', True)], context=context)
                if other_default_committed:
                    raise osv.except_osv(_('Error!'),
                                         _('Only one default commitments version can exist.'))

    def _check_default_plan(self, cr, uid, vals, context=None):

        if 'default_plan' in vals:
            if vals['default_plan'] is True:
                other_default_plan = self.search(cr, uid, [('default_plan', '=', True)], context=context)
                if other_default_plan:
                    raise osv.except_osv(_('Error!'),
                                         _('Only one default planning version can exist.'))

    _defaults = {
        'active': True,
        'company_id': lambda self, cr, uid,
        c: self.pool.get('res.users').browse(cr, uid, uid, c).company_id.id,
        'default_committed': False,
        'default_plan': False,
    }

    def create(self, cr, uid, vals, *args, **kwargs):

        context = kwargs.get('context', {})
        self._check_default_committed(cr, uid, vals, context)
        self._check_default_plan(cr, uid, vals, context)

        res = super(account_analytic_plan_version, self).create(cr, uid, vals, *args, **kwargs)

        return res

    def write(self, cr, uid, ids, vals, context=None):
        if context is None:
            context = {}

        self._check_default_committed(cr, uid, vals, context)
        self._check_default_plan(cr, uid, vals, context)

        return super(account_analytic_plan_version, self).write(cr, uid, ids, vals, context=context)


account_analytic_plan_version()
