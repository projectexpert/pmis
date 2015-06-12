# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp.osv import fields,osv
from openerp import tools

class report_account_analytic_resource_usage(osv.osv):
    _name = "report.account.analytic.resource.usage"
    _description = "Resource Usage Analysis"
    _auto = False
    _columns = {        
        'date': fields.date('Date', readonly=True),
        'day': fields.char('Day', size=128, readonly=True),
        'month':fields.selection([('01','January'), ('02','February'), ('03','March'), ('04','April'), ('05','May'), ('06','June'), ('07','July'), ('08','August'), ('09','September'), ('10','October'), ('11','November'), ('12','December')], 'Month', readonly=True),
        'year': fields.char('Year', size=64, required=False, readonly=True),
        'period_id': fields.many2one('account.period', 'Period', readonly=True),
        'account_id': fields.many2one('account.analytic.account', 'Analytic Account', readonly=True),
        'product_id': fields.many2one('product.product', 'Product', readonly=True),
        'product_uom_id': fields.many2one('product.uom', 'UoM', readonly=True),
        'user_id': fields.many2one('res.users', 'User', readonly=True),
        'amount_plan': fields.float('Planned Amount', readonly=True, help='Calculated by multiplying the quantity and the price given in the Product\'s cost price. Always expressed in the company main currency.'),
        'amount_commit': fields.float('Commited Amount', readonly=True, help='Calculated by multiplying the quantity and the price given in the Product\'s cost price. Always expressed in the company main currency.'),
        'unit_amount_plan': fields.float('Planned Quantity', help='Specifies the amount of quantity to count.'),
        'unit_amount_commit': fields.float('Commited Quantity', help='Specifies the amount of quantity to count.'),
        'amount_real': fields.float('Real Amount', readonly=True, help='Calculated by multiplying the quantity and the price given in the Product\'s cost price. Always expressed in the company main currency.'),
        'unit_amount_real': fields.float('Real Quantity', readonly=True, help='Specifies the amount of quantity to count.'),        
    }


    def init(self, cr):
        
        """ 
            @param cr: the current row, from the database cursor,
        """
        tools.drop_view_if_exists(cr, 'report_account_analytic_resource_usage')
        
        cr.execute("""
            create or replace view report_account_analytic_resource_usage as (
                
              SELECT  
                    ROW_NUMBER() over (order by tot.date) as id,
                    tot.date as date,
                    to_char(tot.date, 'YYYY') as year,
                    to_char(tot.date, 'MM') as month,
                    to_char(tot.date, 'YYYY-MM-DD') as day,
                    sum(tot.unit_amount_real) as unit_amount_real, 
                    sum(tot.unit_amount_plan) as unit_amount_plan, 
                    sum(tot.unit_amount_commit) as unit_amount_commit,
                    sum(tot.amount_real) as amount_real, 
                    sum(tot.amount_plan) as amount_plan,  
                    sum(tot.amount_commit) as amount_commit,
                    tot.period_id, 
                    tot.account_id, 
                    tot.product_id, 
                    tot.product_uom_id, 
                    tot.user_id 
                FROM
                    (SELECT
                         CAST( unit_amount AS FLOAT) AS unit_amount_real, 
                         CAST( 0 AS FLOAT) AS unit_amount_plan, 
                         CAST( 0 AS FLOAT) AS unit_amount_commit,
                         CAST( amount AS FLOAT) AS amount_real, 
                         CAST( 0 AS FLOAT) AS amount_plan,
                         CAST( 0 AS FLOAT) AS amount_commit, 
                         date, 
                         period_id, 
                         account_id, 
                         product_id, 
                         product_uom_id, 
                         user_id 
                    FROM account_analytic_line 

                UNION ALL
                    SELECT 
                        CAST( 0 AS FLOAT) AS unit_amount_real,
                        CAST( unit_amount AS FLOAT) AS unit_amount_plan,
                        CAST( 0 AS FLOAT) AS unit_amount_commit, 
                        CAST( 0 AS FLOAT) AS amount_real, 
                        CAST( amount AS FLOAT) AS amount_plan, 
                        CAST( 0 AS FLOAT) AS amount_commit,
                        date, 
                        period_id, 
                        account_id, 
                        product_id, 
                        product_uom_id, 
                        user_id 
                    FROM account_analytic_line_plan
                UNION ALL
                    SELECT 
                        CAST( 0 AS FLOAT) AS unit_amount_real,
                        CAST( 0 AS FLOAT) AS unit_amount_plan,
                        CAST( unit_amount AS FLOAT) AS unit_amount_commit, 
                        CAST( 0 AS FLOAT) AS amount_real, 
                        CAST( 0 AS FLOAT) AS amount_plan,
                        CAST( amount AS FLOAT) AS amount_commit, 
                        date, 
                        period_id, 
                        account_id, 
                        product_id, 
                        product_uom_id, 
                        user_id 
                    FROM account_analytic_line_commit                    
                    
                ) AS tot
                GROUP BY 
                    tot.date, 
                    tot.period_id, 
                    tot.account_id, 
                    tot.product_id, 
                    tot.product_uom_id, 
                    user_id
                ORDER BY tot.date

            )""")               

        
report_account_analytic_resource_usage()


