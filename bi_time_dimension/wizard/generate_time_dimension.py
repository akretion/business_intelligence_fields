# -*- coding: utf-8 -*-
##############################################################################
#
#    bi_time_dimension module for OpenERP
#    Copyright (C) 2013 Akretion (http://www.akretion.com). All Rights Reserved
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

from osv import osv, fields
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)

# Ideas : map to fiscal year ?

TIME_DIMENSION_TABLE = 'bi_time_dimension'

class generate_time_dimension(osv.osv_memory):
    _name = 'generate.time.dimension'
    _description = 'Generate Time Dimension for OLAP'

    _columns = {
        'start_date': fields.date('Start date', required=True),
        'end_date': fields.date('End date', required=True),
        }

    def _start_before_end(self, cr, uid, ids):
        for wiz in self.browse(cr, uid, ids):
            if wiz.start_date >= wiz.end_date:
                return False
        return True

    _constraints = [
        (_start_before_end, "Start date must be before end date", ['start_date', 'end_date']),
        ]

    def button_run(self, cr, uid, ids, context=None):
        if self.run_generate_table(cr, uid, ids, context=context):
            return {'type': 'ir.actions.act_window_close'}
        else:
            return False

    def run_generate_table(self, cr, uid, ids, context=None):
        query_drop_table = 'DROP TABLE IF EXISTS %s' % TIME_DIMENSION_TABLE
        _logger.debug('Executing SQL = %s' % query_drop_table)
        cr.execute(query_drop_table)

        table_cols = [
        {'name': 'date', 'dbtype': 'DATE PRIMARY KEY'},
        {'name': 'year',     'dbtype': 'VARCHAR(4) NOT NULL'},
        {'name': 'semester', 'dbtype': 'VARCHAR(7) NOT NULL'},
        {'name': 'quarter',  'dbtype': 'VARCHAR(7) NOT NULL'},
        {'name': 'month',    'dbtype': 'VARCHAR(7) NOT NULL'},
        {'name': 'day',      'dbtype': 'VARCHAR(10) NOT NULL'},
        ]

        list_cols_with_type = ''
        list_cols = ''
        i = 1
        for col in table_cols:
            list_cols_with_type += col['name'] + ' ' + col['dbtype']
            list_cols += col['name']
            if i <> len(table_cols):
                list_cols_with_type += ', '
                list_cols += ', '
            i += 1

        #print "list_cols_with_type=", list_cols_with_type

        query_create_table = 'CREATE TABLE %s (%s)' % (TIME_DIMENSION_TABLE, list_cols_with_type)
        _logger.debug('Executing SQL = %s' % query_create_table)
        cr.execute(query_create_table)

        wiz = self.browse(cr, uid, ids[0], context=context)
        start_date_str = wiz.start_date
        end_date_str = wiz.end_date
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

        cur_date = start_date
        while True:
            #_logger.debug("Current date = %s", cur_date)
            # TODO : clean-up this code
            # date as timestamp
#            list_values = "TIMESTAMP '" + cur_date.strftime('%Y-%m-%d') + " 00:00:00'" + ", "

            list_values = "'" + cur_date.strftime('%Y-%m-%d') + "', "
            # Year
            list_values += "'" + cur_date.strftime('%Y') + "', "
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
            # Semester
            month_str = cur_date.strftime('%m')
            list_values += "'" + cur_date.strftime('%Y-') + compute[month_str]['semester'] + "', "
            # Quarter
            list_values += "'" + cur_date.strftime('%Y-') + compute[month_str]['quarter'] + "', "

            # Month
            list_values += "'" + cur_date.strftime('%Y-%m') + "', "
            # Day
            list_values += "'" + cur_date.strftime('%Y-%m-%d') + "'"
            # Insert cur_date in SQL
            query_insert_date = 'INSERT INTO %s (%s) VALUES (%s)' %(TIME_DIMENSION_TABLE, list_cols, list_values)
            _logger.debug('Insert date = %s' % query_insert_date)
            cr.execute(query_insert_date)
            if cur_date == end_date:
                break
            # go to next day
            cur_date += relativedelta(days=1)
        return True
