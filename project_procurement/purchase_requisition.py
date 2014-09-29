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


class purchase_requisition(osv.osv):
    _inherit = "purchase.requisition"

    def copy_data(self, cr, uid, id, default={}, context=None):
        if not default:
            default = {}
        default.update({
            'state':'draft',
            'purchase_ids':[],
            'name': self.pool.get('ir.sequence').get(cr, uid, 'purchase.order.requisition'),
        })
        return super(purchase_requisition, self).copy_data(cr, uid, id, default, context)

    _columns = {        
            #In case that the project is deleted, we also delete this entity
            'project_id':fields.many2one('project.project', 'Project', ondelete='cascade'),       
    }

    def onchange_project_id(self, cr, uid, ids, project_id):
        analytic_account_id = ''
        
        if project_id:            
            project_obj = self.pool.get('project.project')
            #Read the project's analytic account
            analytic_account_id = project_obj.read(cr, uid, project_id,'analytic_account_id')['analytic_account_id']
            
        lines=self.pool.get('purchase.requisition.line')
                
        for pr in self.browse(cr, uid, ids, context=None):            
        #Get the order lines       
            for line in pr.line_ids:                
                lines.write(cr, uid, line.id, {                                                            
                        'account_analytic_id': analytic_account_id,                                                              
                })
                                    
        return {}
            
purchase_requisition()



