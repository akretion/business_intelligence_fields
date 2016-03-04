# -*- coding: utf-8 -*-
##############################################################################
#
#    bi_time_dimension module for Odoo
#    Copyright (C) 2013-2016 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
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

from openerp import models, fields, api, tools, _
from openerp.exceptions import ValidationError
import logging
from dateutil.relativedelta import relativedelta
import psycopg2

logger = logging.getLogger(__name__)
TIME_DIMENSION_TABLE = 'bi_time_dimension'


class GenerateTimeDimension(models.TransientModel):
    _name = 'generate.time.dimension'
    _description = 'Generate Time Dimension for OLAP'

    start_date = fields.Date(string='Start date', required=True)
    end_date = fields.Date(string='End date', required=True)

    @api.one
    @api.constrains('start_date', 'end_date')
    def _start_before_end(self):
        if self.start_date >= self.end_date:
            raise ValidationError(_(
                "Start date must be before end date"))

    @api.multi
    def generate_table(self):
        self.ensure_one()
        bi_dsn = tools.config.get('bi_dsn')
        # bi_dsn should somethink like:
        # host='192.168.12.42' dbname='bi' user='odoo' password='azerty'
        if bi_dsn:
            conn = psycopg2.connect(bi_dsn)
            cr = conn.cursor()
            logger.info('Starting to create BI time dimension in BI database')
        else:
            cr = self._cr
            logger.info(
                'Starting to create BI time dimension in Odoo database')
        query_drop_table = 'DROP TABLE IF EXISTS %s' % TIME_DIMENSION_TABLE
        logger.debug('Executing SQL = %s' % query_drop_table)
        cr.execute(query_drop_table)

        table_cols = [
            {'name': 'date',     'dbtype': 'DATE PRIMARY KEY'},
            {'name': 'year',     'dbtype': 'VARCHAR(4) NOT NULL'},
            {'name': 'fiscal_year', 'dbtype': 'VARCHAR(9) NOT NULL'},
            {'name': 'semester', 'dbtype': 'VARCHAR(7) NOT NULL'},
            {'name': 'quarter',  'dbtype': 'VARCHAR(7) NOT NULL'},
            {'name': 'month',    'dbtype': 'VARCHAR(7) NOT NULL'},
            {'name': 'day',      'dbtype': 'VARCHAR(10) NOT NULL'},
        ]

        list_cols_with_type = ''
        list_cols = ''
        i = 1
        for col in table_cols:
            list_cols_with_type += '%s %s' % (col['name'], col['dbtype'])
            list_cols += col['name']
            if i != len(table_cols):
                list_cols_with_type += ', '
                list_cols += ', '
            i += 1

        query_create_table = 'CREATE TABLE %s (%s)' % (
            TIME_DIMENSION_TABLE, list_cols_with_type)

        logger.debug('Executing create table query: %s' % query_create_table)
        cr.execute(query_create_table)

        start_date_str = self.start_date
        end_date_str = self.end_date
        start_date = fields.Date.from_string(start_date_str)
        end_date = fields.Date.from_string(end_date_str)

        cur_date = start_date
        list_values = []
        afo = self.env['account.fiscalyear']
        fy_idtocode = {}
        for fy in afo.search([]):
            fy_idtocode[fy.id] = fy.code
        while cur_date <= end_date:
            # logger.debug("Current date = %s", cur_date)
            # date as timestamp

            # list_values = "TIMESTAMP '" + cur_date.strftime('%Y-%m-%d')
            # + " 00:00:00'" + ", "
            compute = {
                '01': {'quarter': 'Q1', 'semester': 'S1'},
                '02': {'quarter': 'Q1', 'semester': 'S1'},
                '03': {'quarter': 'Q1', 'semester': 'S1'},
                '04': {'quarter': 'Q2', 'semester': 'S1'},
                '05': {'quarter': 'Q2', 'semester': 'S1'},
                '06': {'quarter': 'Q2', 'semester': 'S1'},
                '07': {'quarter': 'Q3', 'semester': 'S2'},
                '08': {'quarter': 'Q3', 'semester': 'S2'},
                '09': {'quarter': 'Q3', 'semester': 'S2'},
                '10': {'quarter': 'Q4', 'semester': 'S2'},
                '11': {'quarter': 'Q4', 'semester': 'S2'},
                '12': {'quarter': 'Q4', 'semester': 'S2'},
            }
            month_str = cur_date.strftime('%m')
            semester = '%s-%s' % (
                cur_date.strftime('%Y'), compute[month_str]['semester'])
            quarter = '%s-%s' % (
                cur_date.strftime('%Y'), compute[month_str]['quarter'])
            cur_date_str = fields.Date.to_string(cur_date)
            fyear_id = afo.find(dt=cur_date_str, exception=False)

            list_values.append({
                'date': cur_date.strftime('%Y-%m-%d'),
                'year': cur_date.strftime('%Y'),
                'fiscal_year': fyear_id and fy_idtocode[fyear_id] or False,
                'semester': semester,
                'quarter': quarter,
                'month': cur_date.strftime('%Y-%m'),
                'day': cur_date.strftime('%Y-%m-%d'),
            })

            # go to next day
            cur_date += relativedelta(days=1)
        # Insert cur_date in SQL
        # from pprint import pprint
        # pprint(list_values)
        query_insert_date = 'INSERT INTO %s (%s) VALUES (%s)' % (
            TIME_DIMENSION_TABLE, list_cols,
            '%(date)s, %(year)s, %(fiscal_year)s, %(semester)s, '
            '%(quarter)s, %(month)s, %(day)s'
            )
        logger.debug('Insert into queries: %s' % query_insert_date)
        cr.executemany(query_insert_date, list_values)
        logger.info(
            'Successfull creation of the table %s in the database',
            TIME_DIMENSION_TABLE)
        if bi_dsn:
            conn.commit()
            cr.close()
            conn.close()

        return True
