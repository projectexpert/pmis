# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Eficent (<http://www.eficent.com/>)
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
from openerp import tools

class account_analytic_account(osv.osv):
    
    def _categories_name_calc(self, cr, uid, ids, name, args, context=None):
        
        if not ids:
            return []
        res = []            
            
        accounts_br = self.browse(cr, uid, ids, context=context)   
                
        for account in accounts_br:
            data =[]
            categories_br = account.category_id
            if categories_br:                    
                for category_br in categories_br:
                    cat_name = category_br.complete_name or ''
                    data.insert(0, cat_name)
                data.sort(cmp=None, key=None, reverse=False)
                data_str = ', '.join(map(tools.ustr,data))     
                
            else:
                data_str = ''
                                

            res.append((account.id, data_str))
                                   
        return dict(res)     
    
    _inherit = 'account.analytic.account'
    _columns = {   
            
        'category_id': fields.many2many('analytic.account.category', 'analytic_account_category_rel', 'account_id', 'category_id', 'Categories'),
        'categories_name_str': fields.function(_categories_name_calc, method=True, type='text', string='Categories', help='Analytic account categories'), 
                                               
     }
                
account_analytic_account()