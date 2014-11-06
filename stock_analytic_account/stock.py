# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#              Eficent <contact@eficent.com>
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
from openerp.osv import fields, osv, orm

    
class stock_move(osv.osv):    

    _inherit = "stock.move"

    _columns = {        
        'analytic_account_id': fields.many2one('account.analytic.account', 'Analytic Account'),
        'analytic_account_user_id': fields.related('analytic_account_id',
                                           'user_id',
                                           type='many2one',
                                           relation='res.users',
                                           string='Project Manager',
                                           store=True,
                                           readonly=True),
    }
    
stock_move()