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


{
    'name': 'Business intelligence - Time dimension',
    'summary': 'Generate time dimension table for BI',
    'version': '0.1',
    'category': 'Tools',
    'license': 'AGPL-3',
    'description': """This module adds a wizard to generate the time dimension for business intelligence.

By default, it will create the time dimension table in the Odoo database. If you have a bi_dsn entry in your Odoo server configuration file, it will create a time dimension table in the designated external database.

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
""",
    'author': 'Akretion',
    'website': 'http://www.akretion.com/',
    'depends': ['base'],
    'data': ['wizard/generate_time_dimension_view.xml'],
    'installable': False,
}
