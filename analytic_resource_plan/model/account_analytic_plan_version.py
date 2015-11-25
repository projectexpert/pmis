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
from openerp.osv import fields, orm


class AccountAnalyticPlanVersion(orm.Model):
    _inherit = 'account.analytic.plan.version'

    _columns = {
        'default_resource_plan': fields.boolean(
            'Default for resource plan'),
    }

    def _check_default_resource(self, cr, uid, vals, context=None):

        if 'default_resource_plan' in vals:
            if vals['default_resource_plan'] is True:
                other_default_resource = self.search(
                    cr, uid, [('default_resource_plan', '=', True)],
                    context=context)
                if other_default_resource:
                    raise orm.except_orm(_('Error!'),
                                         _('Only one default for resource '
                                           'plan version can exist.'))

    _defaults = {
        'default_resource_plan': False,
    }

    def create(self, cr, uid, vals, *args, **kwargs):

        context = kwargs.get('context', {})
        self._check_default_resource(cr, uid, vals, context)

        res = super(AccountAnalyticPlanVersion, self).create(
            cr, uid, vals, *args, **kwargs)

        return res

    def write(self, cr, uid, ids, vals, context=None):
        if context is None:
            context = {}

        self._check_default_resource(cr, uid, vals, context)

        return super(AccountAnalyticPlanVersion, self).write(
            cr, uid, ids, vals, context=context)
