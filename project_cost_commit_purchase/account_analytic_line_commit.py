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

from lxml import etree
import time
from datetime import datetime, date, timedelta
import decimal_precision as dp
from tools.translate import _
from osv import fields, osv
import netsvc
import tools

class account_analytic_line_commit(osv.osv):
    _inherit = 'account.analytic.line.commit'
    
    _columns = {
        'purchase_line_id': fields.many2one('purchase.order.line', 'Purchase Order Line', ondelete='cascade', select=True),
    }
account_analytic_line_commit()