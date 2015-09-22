# -*- coding: utf-8 -*-
# #############################################################################
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

from openerp.osv import fields, osv
from openerp import tools


class report_account_analytic_plan_actual(osv.osv):
    _name = "report.account.analytic.plan.actual"
    _description = "Plan vs. actual analysis"
    _auto = False
    _columns = {
        'date': fields.date('Date', readonly=True),
        'day': fields.char('Day', size=12, readonly=True),
        'month': fields.selection([('01', 'January'),
                                   ('02', 'February'),
                                   ('03', 'March'),
                                   ('04', 'April'),
                                   ('05', 'May'),
                                   ('06', 'June'),
                                   ('07', 'July'),
                                   ('08', 'August'),
                                   ('09', 'September'),
                                   ('10', 'October'),
                                   ('11', 'November'),
                                   ('12', 'December')],
                                  'Month', readonly=True),
        'year': fields.char(
            'Year', size=64, required=False, readonly=True
        ),
        'account_id': fields.many2one(
            'account.analytic.account', 'Analytic Account', readonly=True
        ),
        'complete_wbs_code': fields.related(
            'account_id', 'complete_wbs_code',
            type='char', size=250,
            string='Full WBS Code', store=True
        ),
        'complete_wbs_name': fields.related(
            'account_id', 'complete_wbs_name',
            type='char', size=250,
            string='Full WBS Name', store=True
        ),
        'kpi_type': fields.selection([('PC', 'Cost - Plan'),
                                      ('AC', 'Cost - Actual'),
                                      ('PR', 'Revenue - Plan'),
                                      ('AR', 'Revenue - Actual'),
                                      ('PB', 'Gross Margin - Plan'),
                                      ('AB', 'Gross Margin - Actual'),
                                      ('CV', 'Cost - Variance'),
                                      ('RV', 'Revenue - Variance'),
                                      ('BV', 'Gross Margin - Variance')],
                                     'Type', size=12, readonly=True),
        'kpi_amount': fields.float('Amount'),
        'version_id': fields.many2one(
            'account.analytic.plan.version', 'Planning Version', readonly=True
        ),
        'product_id': fields.many2one(
            'product.product', 'Product', readonly=True
        ),
        'product_uom_id': fields.many2one('product.uom', 'UoM', readonly=True),
        'general_account_id': fields.many2one(
            'account.account', 'General Account', readonly=True
        ),

    }

    _order = 'date'

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
                    tot.account_id,
                    tot.complete_wbs_code,
                    tot.complete_wbs_name,
                    tot.kpi_type,
                    sum(tot.kpi_amount) as kpi_amount,
                    tot.product_id,
                    tot.product_uom_id,
                    tot.version_id,
                    tot.general_account_id
                FROM
                    (SELECT
                         CAST(AAL.amount AS FLOAT) AS kpi_amount,
                         'AC'::text AS kpi_type,
                         AAL.date,
                         AAL.account_id,
                         AAC.complete_wbs_code,
                         AAC.complete_wbs_name,
                         AAL.product_id,
                         AAL.product_uom_id,
                         AAL.general_account_id,
                         AAPV.id AS version_id
                    FROM account_analytic_line AAL
                    INNER JOIN account_analytic_account AAC
                    ON AAL.account_id = AAC.id
                    INNER JOIN account_account AC
                    ON AAL.general_account_id = AC.id
                    INNER JOIN account_account_type AT
                    ON AT.id = AC.user_type,
                    account_analytic_plan_version AAPV
                    WHERE AT.report_type = 'expense'

                UNION ALL
                    SELECT
                         CAST(AAL.amount AS FLOAT) AS kpi_amount,
                         'AR'::text AS kpi_type,
                         AAL.date,
                         AAL.account_id,
                         AAC.complete_wbs_code,
                         AAC.complete_wbs_name,
                         AAL.product_id,
                         AAL.product_uom_id,
                         AAL.general_account_id,
                         AAPV.id AS version_id
                    FROM account_analytic_line AAL
                    INNER JOIN account_analytic_account AAC
                    ON AAL.account_id = AAC.id
                    INNER JOIN account_account AC
                    ON AAL.general_account_id = AC.id
                    INNER JOIN account_account_type AT
                    ON AT.id = AC.user_type,
                    account_analytic_plan_version AAPV
                    WHERE AT.report_type = 'income'

                UNION ALL
                    SELECT
                         CAST(AALP.amount AS FLOAT) AS kpi_amount,
                         'PC'::text AS kpi_type,
                         AALP.date,
                         AALP.account_id,
                         AAC.complete_wbs_code,
                         AAC.complete_wbs_name,
                         AALP.product_id,
                         AALP.product_uom_id,
                         AALP.general_account_id,
                         AALP.version_id
                    FROM account_analytic_line_plan as AALP
                    INNER JOIN account_analytic_account AAC
                    ON AALP.account_id = AAC.id
                    INNER JOIN account_account AC
                    ON AALP.general_account_id = AC.id
                    INNER JOIN account_account_type AT
                    ON AT.id = AC.user_type
                    WHERE AT.report_type = 'expense'

                UNION ALL
                    SELECT
                         CAST(AALP.amount AS FLOAT) AS kpi_amount,
                         'PR'::text AS kpi_type,
                         AALP.date,
                         AALP.account_id,
                         AAC.complete_wbs_code,
                         AAC.complete_wbs_name,
                         AALP.product_id,
                         AALP.product_uom_id,
                         AALP.general_account_id,
                         AALP.version_id
                    FROM account_analytic_line_plan as AALP
                    INNER JOIN account_analytic_account AAC
                    ON AALP.account_id = AAC.id
                    INNER JOIN account_account AC
                    ON AALP.general_account_id = AC.id
                    INNER JOIN account_account_type AT
                    ON AT.id = AC.user_type
                    WHERE AT.report_type = 'income'

                UNION ALL
                    SELECT
                         CAST( AALP.amount AS FLOAT) AS kpi_amount,
                         'CV'::text AS kpi_type,
                         AALP.date,
                         AALP.account_id,
                         AAC.complete_wbs_code,
                         AAC.complete_wbs_name,
                         AALP.product_id,
                         AALP.product_uom_id,
                         AALP.general_account_id,
                         AALP.version_id
                    FROM account_analytic_line_plan as AALP
                    INNER JOIN account_analytic_account AAC
                    ON AALP.account_id = AAC.id
                    INNER JOIN account_account AC
                    ON AALP.general_account_id = AC.id
                    INNER JOIN account_account_type AT
                    ON AT.id = AC.user_type
                    WHERE AT.report_type = 'expense'

                UNION ALL
                    SELECT
                         CAST( -1 * AAL.amount AS FLOAT) AS kpi_amount,
                         'CV'::text AS kpi_type,
                         AAL.date,
                         AAL.account_id,
                         AAC.complete_wbs_code,
                         AAC.complete_wbs_name,
                         AAL.product_id,
                         AAL.product_uom_id,
                         AAL.general_account_id,
                         AAPV.id AS version_id
                    FROM account_analytic_line as AAL
                    INNER JOIN account_analytic_account AAC
                    ON AAL.account_id = AAC.id
                    INNER JOIN account_account AC
                    ON AAL.general_account_id = AC.id
                    INNER JOIN account_account_type AT
                    ON AT.id = AC.user_type,
                    account_analytic_plan_version AAPV
                    WHERE AT.report_type = 'expense'

                UNION ALL
                    SELECT
                         CAST( AALP.amount AS FLOAT) AS kpi_amount,
                         'RV'::text AS kpi_type,
                         AALP.date,
                         AALP.account_id,
                         AAC.complete_wbs_code,
                         AAC.complete_wbs_name,
                         AALP.product_id,
                         AALP.product_uom_id,
                         AALP.general_account_id,
                         AALP.version_id
                    FROM account_analytic_line_plan AS AALP
                    INNER JOIN account_analytic_account AAC
                    ON AALP.account_id = AAC.id
                    INNER JOIN account_account AC
                    ON AALP.general_account_id = AC.id
                    INNER JOIN account_account_type AT
                    ON AT.id = AC.user_type
                    WHERE AT.report_type = 'income'

                UNION ALL
                    SELECT
                         CAST( -1 * AAL.amount AS FLOAT) AS kpi_amount,
                         'RV'::text AS kpi_type,
                         AAL.date,
                         AAL.account_id,
                         AAC.complete_wbs_code,
                         AAC.complete_wbs_name,
                         AAL.product_id,
                         AAL.product_uom_id,
                         AAL.general_account_id,
                         AAPV.id AS version_id
                    FROM account_analytic_line AS AAL
                    INNER JOIN account_analytic_account AAC
                    ON AAL.account_id = AAC.id
                    INNER JOIN account_account AC
                    ON AAL.general_account_id = AC.id
                    INNER JOIN account_account_type AT
                    ON AT.id = AC.user_type,
                    account_analytic_plan_version AAPV
                    WHERE AT.report_type = 'income'

                UNION ALL
                    SELECT
                         CAST(AALP.amount AS FLOAT) AS kpi_amount,
                         'PB'::text AS kpi_type,
                         AALP.date,
                         AALP.account_id,
                         AAC.complete_wbs_code,
                         AAC.complete_wbs_name,
                         AALP.product_id,
                         AALP.product_uom_id,
                         AALP.general_account_id,
                         AALP.version_id
                    FROM account_analytic_line_plan AS AALP
                    INNER JOIN account_analytic_account AAC
                    ON AALP.account_id = AAC.id
                    INNER JOIN account_account AC
                    ON AALP.general_account_id = AC.id
                    INNER JOIN account_account_type AT
                    ON AT.id = AC.user_type
                    WHERE AT.report_type IN ('expense', 'income')

                UNION ALL
                    SELECT
                         CAST(AAL.amount AS FLOAT) AS kpi_amount,
                         'AB'::text AS kpi_type,
                         AAL.date,
                         AAL.account_id,
                         AAC.complete_wbs_code,
                         AAC.complete_wbs_name,
                         AAL.product_id,
                         AAL.product_uom_id,
                         AAL.general_account_id,
                         AAPV.id AS version_id
                    FROM account_analytic_line AS AAL
                    INNER JOIN account_analytic_account AAC
                    ON AAL.account_id = AAC.id
                    INNER JOIN account_account AC
                    ON AAL.general_account_id = AC.id
                    INNER JOIN account_account_type AT
                    ON AT.id = AC.user_type,
                    account_analytic_plan_version AAPV
                    WHERE AT.report_type IN ('expense', 'income')

                UNION ALL
                    SELECT
                         CAST( AALP.amount AS FLOAT) AS kpi_amount,
                         'BV'::text AS kpi_type,
                         AALP.date,
                         AALP.account_id,
                         AAC.complete_wbs_code,
                         AAC.complete_wbs_name,
                         AALP.product_id,
                         AALP.product_uom_id,
                         AALP.general_account_id,
                         AALP.version_id
                    FROM account_analytic_line_plan as AALP
                    INNER JOIN account_analytic_account AAC
                    ON AALP.account_id = AAC.id
                    INNER JOIN account_account AC
                    ON AALP.general_account_id = AC.id
                    INNER JOIN account_account_type AT
                    ON AT.id = AC.user_type
                    WHERE AT.report_type IN ('expense', 'income')

                UNION ALL
                    SELECT
                         CAST( -1 * AAL.amount AS FLOAT) AS kpi_amount,
                         'BV'::text AS kpi_type,
                         AAL.date,
                         AAL.account_id,
                         AAC.complete_wbs_code,
                         AAC.complete_wbs_name,
                         AAL.product_id,
                         AAL.product_uom_id,
                         AAL.general_account_id,
                         AAPV.id AS version_id
                    FROM account_analytic_line as AAL
                    INNER JOIN account_analytic_account AAC
                    ON AAL.account_id = AAC.id
                    INNER JOIN account_account AC
                    ON AAL.general_account_id = AC.id
                    INNER JOIN account_account_type AT
                    ON AT.id = AC.user_type,
                    account_analytic_plan_version AAPV
                    WHERE AT.report_type IN ('expense', 'income')
                ) AS tot
                GROUP BY
                    tot.date,
                    tot.account_id,
                    tot.complete_wbs_code,
                    tot.complete_wbs_name,
                    tot.kpi_type,
                    tot.product_id,
                    tot.product_uom_id,
                    tot.general_account_id,
                    tot.version_id
                ORDER BY tot.date

            )""")


report_account_analytic_plan_actual()
