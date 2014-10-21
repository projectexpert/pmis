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


class report_account_analytic_plan_actual(osv.osv):
    _name = "report.account.analytic.plan.actual"
    _description = "Plan vs. actual analysis"
    _auto = False
    _columns = {        
        'date': fields.date('Date', readonly=True),        
        'month':fields.selection([('01','January'), ('02','February'), ('03','March'), ('04','April'), ('05','May'), ('06','June'), ('07','July'), ('08','August'), ('09','September'), ('10','October'), ('11','November'), ('12','December')], 'Month', readonly=True),
        'year': fields.char('Year', size=64, required=False, readonly=True),
        'account_id': fields.many2one('account.analytic.account', 'Analytic Account', readonly=True),        
        'kpi_type': fields.selection([('PC', 'Planned Cost'),
                                      ('AC','Actual Cost'),
                                      ('PR','Planned Revenue'),
                                      ('AR','Actual Revenue'),
                                      ('CV','Cost variance'),
                                      ('RV','Revenue variance')]
                                     , 'Type',  size=12, readonly=True),                
        'kpi_amount': fields.float('Amount'),        
        'version_id': fields.many2one('account.analytic.plan.version', 'Planning Version', readonly=True),
        'product_id': fields.many2one('product.product', 'Product', readonly=True),
        'product_uom_id': fields.many2one('product.uom', 'UoM', readonly=True),        
                
    }


    def init(self, cr):
        
        """ 
            @param cr: the current row, from the database cursor,
        """
        tools.drop_view_if_exists(cr, 'report_account_analytic_plan_actual')
        
        cr.execute("""
            create or replace view report_account_analytic_plan_actual as (
                
              SELECT  
                    ROW_NUMBER() over (order by tot.date) as id,
                    tot.date as date,
                    to_char(tot.date, 'YYYY') as year,
                    to_char(tot.date, 'MM') as month,
                    to_char(tot.date, 'YYYY-MM-DD') as day,                    
                    tot.account_id, 
                    tot.kpi_type,
                    sum(tot.kpi_amount) as kpi_amount,
                    tot.product_id,
                    tot.product_uom_id,
                    tot.version_id
                FROM
                    (SELECT                    
                         CAST( abs(amount) AS FLOAT) AS kpi_amount, 
                         'AC' AS kpi_type,                          
                         date, 
                         account_id,
                         product_id,      
                         product_uom_id,                    
                         CAST(0 AS INT) AS version_id                         
                    FROM account_analytic_line 
                    WHERE amount < 0

                UNION ALL
                    SELECT                    
                         CAST( abs(amount) AS FLOAT) AS kpi_amount, 
                         'AR' AS kpi_type,                          
                         date, 
                         account_id,     
                         product_id,
                         product_uom_id,
                         CAST(0 AS INT) AS version_id                         
                    FROM account_analytic_line 
                    WHERE amount > 0
            
                UNION ALL
                    SELECT                    
                         CAST( abs(amount) AS FLOAT) AS kpi_amount, 
                         'PC' AS kpi_type,                          
                         date, 
                         account_id,     
                         product_id,      
                         product_uom_id,               
                         version_id                         
                    FROM account_analytic_line_plan 
                    WHERE amount < 0

                UNION ALL
                    SELECT                    
                         CAST( abs(amount) AS FLOAT) AS kpi_amount, 
                         'PR' AS kpi_type,                          
                         date, 
                         account_id, 
                         product_id,
                         product_uom_id,                         
                         version_id                         
                    FROM account_analytic_line_plan 
                    WHERE amount > 0

                UNION ALL
                    SELECT                    
                         CAST( amount AS FLOAT) AS kpi_amount, 
                         'CV' AS kpi_type,                          
                         date, 
                         account_id,  
                         product_id,     
                         product_uom_id,                   
                         version_id                         
                    FROM account_analytic_line_plan 
                    WHERE amount < 0

                UNION ALL
                    SELECT                    
                         CAST( amount AS FLOAT) AS kpi_amount, 
                         'CV' AS kpi_type,                          
                         date, 
                         account_id,      
                         product_id,
                         product_uom_id,                    
                         CAST(0 AS INT) AS version_id                      
                    FROM account_analytic_line
                    WHERE amount < 0

                UNION ALL
                    SELECT                    
                         CAST( amount AS FLOAT) AS kpi_amount, 
                         'RV' AS kpi_type,                          
                         date, 
                         account_id,      
                         product_id,
                         product_uom_id,                    
                         version_id                         
                    FROM account_analytic_line_plan
                    WHERE amount > 0

                UNION ALL
                    SELECT                    
                         CAST( amount AS FLOAT) AS kpi_amount, 
                         'RV' AS kpi_type,                          
                         date, 
                         account_id,
                         product_id,    
                         product_uom_id,                      
                         CAST(0 AS INT) AS version_id                     
                    FROM account_analytic_line
                    WHERE amount > 0                                      
                                                                  
                ) AS tot
                GROUP BY 
                    tot.date, 
                    tot.account_id,
                    tot.kpi_type, 
                    tot.product_id,
                    tot.product_uom_id,
                    tot.version_id
                ORDER BY tot.date

            )""")               

        
report_account_analytic_plan_actual()


