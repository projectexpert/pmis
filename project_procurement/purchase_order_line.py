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


import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

from osv import osv, fields
import netsvc
import pooler
from tools.translate import _
import decimal_precision as dp
from osv.orm import browse_record, browse_null


class purchase_order_line(osv.osv):
    
    _inherit = "purchase.order.line"
  
    _columns = {
        'order_project_id': fields.related('order_id', 'project_id', type='many2one', relation='project.project', store=True, string='Project'),
    }

   
    def create(self, cr, uid, vals, *args, **kwargs):
        if 'order_id' in vals:
            order_obj= self.pool.get('purchase.order').browse(cr, uid, vals['order_id'], context=None)
        
        analytic_account_id = ''
        
        if order_obj.project_id:            
            project_obj = self.pool.get('project.project')
            #Read the project's analytic account
            analytic_account_id = project_obj.read(cr, uid, order_obj.project_id.id,'analytic_account_id')['analytic_account_id']
            vals['account_analytic_id'] = analytic_account_id
            
        return super(purchase_order_line,self).create(cr, uid, vals, *args, **kwargs)

    def button_cancel(self, cr, uid, ids, context=None):
        for line in self.browse(cr, uid, ids, context=context):
            if line.invoiced:
                raise osv.except_osv(_('Invalid action !'), _('You cannot cancel a purchase order line that has already been invoiced !'))
            for move_line in line.move_ids:
                if move_line.state != 'cancel':
                    raise osv.except_osv(
                            _('Could not cancel purchase order line!'),
                            _('You must first cancel stock moves attached to this purchase order line.'))
        return self.write(cr, uid, ids, {'state': 'cancel'})

    def button_confirm(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'confirmed'})

    def button_done(self, cr, uid, ids, context=None):
        wf_service = netsvc.LocalService("workflow")
        res = self.write(cr, uid, ids, {'state': 'done'})
        for line in self.browse(cr, uid, ids, context=context):
            wf_service.trg_write(uid, 'purchase.order', line.order_id.id, cr)
        return res
    
    
purchase_order_line()