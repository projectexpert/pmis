# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Eficent (<http://www.eficent.com/>)
#               <contact@eficent.com>
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

from openerp import models


class AnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    def _compute_scheduled_dates(self, cr, uid, analytic, context=None):
        # Obtain the earliest and latest dates of the children
        start_dates = []
        end_dates = []
        if not analytic.child_ids:
            return True
        for child in analytic.child_ids:
            if child.date_start:
                start_dates.append(child.date_start)
            if child.date:
                end_dates.append(child.date)
        min_start_date = False
        max_end_date = False
        if start_dates:
            min_start_date = min(start_dates)
        if end_dates:
            max_end_date = max(end_dates)
        vals = {
            'date_start': min_start_date,
            'date': max_end_date,
        }
        self.write(cr, uid, [analytic.id], vals, context=context)
        return True

    def create(self, cr, uid, values, context=None):
        acc_id = super(AnalyticAccount, self).create(
            cr, uid, values, context=context)
        acc = self.browse(cr, uid, acc_id, context=context)
        self._compute_scheduled_dates(cr, uid, acc.parent_id, context=context)
        return acc_id

    def write(self, cr, uid, ids, vals, context=None):
        res = super(AnalyticAccount, self).write(
            cr, uid, ids, vals, context=context)
        if 'date_start' in vals or 'date' in vals:
            for acc in self.browse(cr, uid, ids, context=context):
                if not acc.parent_id:
                    return res
                self._compute_scheduled_dates(
                    cr, uid, acc.parent_id, context=context)
        return res
