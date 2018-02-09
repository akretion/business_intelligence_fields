# -*- coding: utf-8 -*-
# Copyright (C) 2013-2018 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields, api, tools, _
from odoo.exceptions import ValidationError, UserError
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

    @api.constrains('start_date', 'end_date')
    def _start_before_end(self):
        for wiz in self:
            if wiz.start_date >= wiz.end_date:
                raise ValidationError(_(
                    "Start date must be before end date"))

    def generate_table(self):
        self.ensure_one()
        bi_dsn = tools.config.get('bi_dsn')
        if not bi_dsn:
            raise UserError(_("Missing bi_dsn key in Odoo server config file"))
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
            {'name': 'semester', 'dbtype': 'VARCHAR(7) NOT NULL'},
            {'name': 'quarter',  'dbtype': 'VARCHAR(7) NOT NULL'},
            {'name': 'month',    'dbtype': 'VARCHAR(7) NOT NULL'},
            {'name': 'week',     'dbtype': 'VARCHAR(8) NOT NULL'},
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
            year_str = cur_date.strftime('%Y')
            week_str = unicode(cur_date.isocalendar()[1]).zfill(2)

            list_values.append({
                'date': cur_date.strftime('%Y-%m-%d'),
                'year': year_str,
                'semester': semester,
                'quarter': quarter,
                'month': cur_date.strftime('%Y-%m'),
                'week': '%s-W%s' % (year_str, week_str),
                'day': cur_date.strftime('%Y-%m-%d'),
            })

            # go to next day
            cur_date += relativedelta(days=1)
        # Insert cur_date in SQL
        # from pprint import pprint
        # pprint(list_values)
        query_insert_date = 'INSERT INTO %s (%s) VALUES (%s)' % (
            TIME_DIMENSION_TABLE, list_cols,
            '%(date)s, %(year)s, %(semester)s, '
            '%(quarter)s, %(month)s, %(week)s, %(day)s'
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
