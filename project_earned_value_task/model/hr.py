# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Eficent (<http://www.eficent.com/>)
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

from openerp import models, api, exceptions, _
from datetime import datetime
from datetime import datetime as dt
from dateutil.rrule import *

class HrEmployee(models.Model):
    
    _inherit = "hr.employee"

    @api.model
    def get_employee_cost(self, user_id):
        employee_ids = self.search([('user_id', '=', user_id)])
        if not employee_ids:
            raise exceptions.Warning(
                _('Error!:: No employee is assigned to user.'))
        for employee in employee_ids:
            if not employee.product_id:
                raise exceptions.Warning(
                    _('Error!:: No product is assigned to employee %s.'),
                    (employee.name,))
            return employee.product_id.standard_price

