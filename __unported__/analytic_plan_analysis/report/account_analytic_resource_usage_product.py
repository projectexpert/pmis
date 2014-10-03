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

from osv import fields,osv
import tools

class report_account_analytic_resource_usage_product(osv.osv):
    _name = "report.account.analytic.resource.usage.product"
    _description = "Resource Usage Analysis by Product"
    _auto = False
    _columns = { 
        'date': fields.date('Date', readonly=True),
        'month':fields.selection([('01','January'), ('02','February'), ('03','March'), ('04','April'), ('05','May'), ('06','June'), ('07','July'), ('08','August'), ('09','September'), ('10','October'), ('11','November'), ('12','December')], 'Month', readonly=True),
        'year': fields.char('Year', size=64, required=False, readonly=True),                       
        'account_id': fields.many2one('account.analytic.account', 'Analytic Account', readonly=True),
        'product_id': fields.many2one('product.product', 'Product', readonly=True),
        'product_uom_id': fields.many2one('product.uom', 'UoM', readonly=True),        
        'amount_real': fields.float('Real Balance', readonly=True, help='Calculated by multiplying the quantity and the price given in the Product\'s cost price. Always expressed in the company main currency.'),        
        'amount_debit_real': fields.float('Real Debit', readonly=True, help='Calculated by multiplying the quantity and the price given in the Product\'s cost price. Always expressed in the company main currency.'),
        'amount_credit_real': fields.float('Real Credit', readonly=True, help='Calculated by multiplying the quantity and the price given in the Product\'s cost price. Always expressed in the company main currency.'),
        'amount_plan': fields.float('Planned Balance', readonly=True, help='Calculated by multiplying the quantity and the price given in the Product\'s cost price. Always expressed in the company main currency.'),
        'amount_debit_plan': fields.float('Planned Debit', readonly=True, help='Calculated by multiplying the quantity and the price given in the Product\'s cost price. Always expressed in the company main currency.'),
        'amount_credit_plan': fields.float('Planned Credit', readonly=True, help='Calculated by multiplying the quantity and the price given in the Product\'s cost price. Always expressed in the company main currency.'),                
        'unit_amount_real': fields.float('Real Quantity', readonly=True, help='Specifies the amount of quantity to count.'),
        'unit_amount_plan': fields.float('Planned Quantity', help='Specifies the amount of quantity to count.'),
        'amount_debit_real_plan': fields.float('Plan to Real debit deviation', readonly=True),
        'amount_credit_plan_real': fields.float('Plan to Real credit deviation', readonly=True),
        'amount_real_plan': fields.float('Real to Planned deviation', readonly=True),         
        'version_id': fields.many2one('account.analytic.plan.version', 'Planning Version', readonly=True),
    }


    def init(self, cr):
        
        """ 
            @param cr: the current row, from the database cursor,
        """
        tools.drop_view_if_exists(cr, 'report_account_analytic_resource_usage_product')
        
        cr.execute("""
            create or replace view report_account_analytic_resource_usage_product as (
                SELECT  
                    ROW_NUMBER() over (order by tot.account_id) as id,
                    tot.date,
                    tot.month,
                    tot.year,
                    sum(tot.unit_amount_real) as unit_amount_real, 
                    sum(tot.unit_amount_plan) as unit_amount_plan,                     
                    sum(tot.amount_real) as amount_real,
                    sum(CASE WHEN tot.amount_real > 0
                         THEN tot.amount_real
                         ELSE 0.0
                         END) as amount_debit_real, 
                    sum(CASE WHEN tot.amount_real < 0
                         THEN -tot.amount_real
                         ELSE 0.0
                         END) as amount_credit_real,       
                    sum(tot.amount_plan) as amount_plan,                        
                    sum(CASE WHEN tot.amount_plan > 0
                         THEN tot.amount_plan
                         ELSE 0.0
                         END) as amount_debit_plan,  
                    sum(CASE WHEN tot.amount_plan < 0
                         THEN -tot.amount_plan
                         ELSE 0.0
                         END) as amount_credit_plan,       
                    (sum(CASE WHEN tot.amount_plan < 0
                         THEN -tot.amount_plan
                         ELSE 0.0
                         END)-
                         sum(CASE WHEN tot.amount_real < 0
                         THEN -tot.amount_real
                         ELSE 0.0
                         END)
                         ) as amount_credit_plan_real,
                    (sum(CASE WHEN tot.amount_real > 0
                         THEN tot.amount_real
                         ELSE 0.0
                         END)-
                         sum(CASE WHEN tot.amount_plan > 0
                         THEN tot.amount_plan
                         ELSE 0.0
                         END)                         
                         ) as amount_debit_real_plan,   
                    (sum(tot.amount_plan)-
                         sum(tot.amount_real)                         
                         ) as amount_real_plan,                            
                    tot.account_id,
                    tot.product_uom_id,                   
                    tot.product_id,
                    tot.version_id
                FROM
                    (SELECT
                         date,
                         to_char(date, 'YYYY') as year,
                         to_char(date, 'MM') as month,
                         CAST( unit_amount AS FLOAT) AS unit_amount_real, 
                         CAST( 0 AS FLOAT) AS unit_amount_plan, 
                         CAST( amount AS FLOAT) AS amount_real, 
                         CAST( 0 AS FLOAT) AS amount_plan,                      
                         account_id, 
                         product_id, 
                         product_uom_id,
                         CAST(0 AS INT) AS version_id
                    FROM account_analytic_line 

                UNION ALL
                    SELECT 
                        date,
                        to_char(date, 'YYYY') as year,
                        to_char(date, 'MM') as month,
                        CAST( 0 AS FLOAT) AS unit_amount_real,
                        CAST( unit_amount AS FLOAT) AS unit_amount_plan, 
                        CAST( 0 AS FLOAT) AS amount_real, 
                        CAST( amount AS FLOAT) AS amount_plan, 
                        account_id, 
                        product_id, 
                        product_uom_id,
                        version_id
                    FROM account_analytic_line_plan
                ) AS tot
                GROUP BY
                    tot.date,
                    tot.year,
                    tot.month,
                    tot.account_id,
                    tot.product_uom_id,
                    tot.product_id,
                    tot.version_id                                        
                ORDER BY tot.account_id

            )""")               

        
report_account_analytic_resource_usage_product()


