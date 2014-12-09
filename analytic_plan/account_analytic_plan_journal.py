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
from openerp.osv import fields, osv

class account_analytic_plan_journal(osv.osv):
    
    _name = 'account.analytic.plan.journal'
    _description = 'Analytic Journal Plan'
    _columns = {
        'name': fields.char('Planning Journal Name', size=64, required=True),
        'code': fields.char('Planning Journal Code', size=8),
        'active': fields.boolean('Active', help="If the active field is set to False, "
                                                "it will allow you to hide the analytic journal "
                                                "without removing it."),
        'type': fields.selection([('sale', 'Sale'),
                                  ('purchase', 'Purchase'),
                                  ('cash', 'Cash'),
                                  ('general', 'General'),
                                  ('situation', 'Situation')],
                                 'Type', size=32, required=True,
                                 help="Gives the type of the analytic journal. "
                                      "When it needs for a document (eg: an invoice) "
                                      "to create analytic entries, OpenERP will look "
                                      "for a matching journal of the same type."),
        'line_ids': fields.one2many('account.analytic.line.plan', 'journal_id', 'Lines'),
        'company_id': fields.many2one('res.company', 'Company', required=True),
        'analytic_journal': fields.many2one('account.analytic.journal', 'Actual Analytic journal', required=False),
        
    }
    _defaults = {
        'active': True,
        'type': 'general',
        'company_id': lambda self, cr, uid, c: self.pool.get('res.users').browse(cr, uid, uid, c).company_id.id,
    }

account_analytic_plan_journal()