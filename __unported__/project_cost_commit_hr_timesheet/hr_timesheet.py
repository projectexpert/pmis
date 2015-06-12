# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Eficent (<http://www.eficent.com/>)
#              Jordi Ballester Alomar <jordi.ballester@eficent.com>
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


from openerp.osv import fields
from openerp.osv import osv


class hr_employee(osv.osv):
    _name = "hr.employee"
    _inherit = "hr.employee"
    _columns = {        
        'commitment_journal_id': fields.many2one('account.analytic.journal.commit', 'Analytic Commitment Journal'),
    }

    def _getAnalyticCommitmentJournal(self, cr, uid, context=None):
        md = self.pool.get('ir.model.data')
        try:
            result = md.get_object_reference(cr, uid, 'hr_timesheet', 'analytic_commitment_journal')
            return result[1]
        except ValueError:
            pass
        return False
    
    _defaults = {
        'commitment_journal_id': _getAnalyticCommitmentJournal,
        
    }

hr_employee()

class hr_analytic_timesheet(osv.osv):

    _inherit = "hr.analytic.timesheet"

    _columns = {
        'line_commit_id': fields.one2many('account.analytic.line.commit', 'hr_timesheet_id', 'Commitment Analytic line'),        
    }


    def _getAnalyticCommitmentJournal(self, cr, uid, context=None):
        emp_obj = self.pool.get('hr.employee')
        if context is None:
            context = {}
        emp_id = emp_obj.search(cr, uid, [('user_id', '=', context.get('user_id', uid))], context=context)
        if emp_id:
            emp = emp_obj.browse(cr, uid, emp_id[0], context=context)
            if emp.commitment_journal_id:
                return emp.commitment_journal_id.id
        return False
    
    def wkf_analytic_line_commit(self, cr, uid, ids, context=None):
        acc_ana_line_obj = self.pool.get('account.analytic.line.commit')
        for obj in self.browse(cr, uid, ids, context=context):
            vals_lines = {
                'name': obj.name,
                'date': obj.date,
                'account_id': obj.account_id and obj.account_id.id or False,
                'unit_amount': obj.unit_amount,
                'product_id': obj.product_id and obj.product_id.id or False,
                'product_uom_id': obj.product_uom_id and obj.product_uom_id.id or False,
                'amount': obj.amount,
                'general_account_id': obj.general_account_id and obj.general_account_id.id or False,
                'journal_id': self._getAnalyticCommitmentJournal(cr,uid,context=context),
                'ref': obj.ref,                    
                'user_id': obj.user_id and obj.user_id.id or False,                    
                'currency_id': obj.currency_id and obj.currency_id.id or False,
                'amount_currency': obj.amount_currency, 
                'hr_timesheet_id': obj.id,
            }    
            
            if obj.line_commit_id:
                for commit_line_id in obj.line_commit_id:
                    acc_ana_line_obj.write(cr, uid, [commit_line_id.id], vals_lines, context=context)
            else:
                acc_ana_line_obj.create(cr, uid, vals_lines, context=context)


        
    def write(self, cr, uid, ids, vals, context=None):
        res = super(hr_analytic_timesheet, self).write(cr, uid, ids, vals, context=context)
            
        self.wkf_analytic_line_commit(cr, uid, ids, context=context)
        
        return res
    
        
    def unlink(self, cr, uid, ids, context=None):
        toremove = {}
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.line_commit_id:
                for line in obj.line_commit_id:
                    toremove[line.id] = True
        if toremove:
            self.pool.get('account.analytic.line.commit').unlink(cr, uid, toremove.keys(), context=context)
        return super(hr_analytic_timesheet, self).unlink(cr, uid, ids, context=context)


hr_analytic_timesheet()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
