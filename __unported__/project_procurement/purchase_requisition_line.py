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

from openerp.osv import fields, osv

class purchase_requisition_line(osv.osv):
    
    _inherit = "purchase.requisition.line"

    def _account_analytic_id(self, cr, uid, ids, name, arg, context=None):                
        purchase_requisition_obj = self.pool.get('purchase.requisition')
        for preq in purchase_requisition_obj.browse(cr, uid, ids, context=context):       
            proj_id = preq.project_id
                
        if proj_id:            
            project_obj = self.pool.get('project.project').browse(cr, uid, proj_id.id, context=context)
            analytic_account_obj = self.pool.get('account.analytic.account').browse(cr, uid, project_obj.analytic_account_id.id, context=context)                           
            value = {'account_analytic_id': analytic_account_obj}
            return {'value': value}                          
                    
        else:
            return {}
    
    _columns = {                    
            'account_analytic_id': fields.function(_account_analytic_id, method=True, string='Account Analytic id',
            type='many2one', relation='account.analytic.account'),
                    
    }
    
    

    
    
purchase_requisition_line()