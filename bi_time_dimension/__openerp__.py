# -*- encoding: utf-8 -*-
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


{
    'name': 'Business intelligence - Time dimension',
    'version': '0.1',
    'category': 'Generic Modules/Others',
    'license': 'AGPL-3',
    'complexity': 'easy',
    'description': """This module adds a wizard to generate the time dimension for OLAP.

Please contact Alexis de Lattre from Akretion <alexis.delattre@akretion.com> for any help or question about this module.
""",
    'author': 'Akretion',
    'website': 'http://www.akretion.com/',
    'depends': ['base'],
    'init_xml': [],
    'update_xml': ['wizard/generate_time_dimension_view.xml'],
    'demo_xml': [],
    'installable': True,
    'active': False,
}

