# -*- encoding: utf-8 -*-
##############################################################################
#
#    bi_product_category module for OpenERP
#    Copyright (C) 2013-2014 Akretion (http://www.akretion.com)
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
    'name': 'Business Intelligence - Product category',
    'version': '0.1',
    'category': 'Business Intelligence',
    'license': 'AGPL-3',
    'description': """This module adds some fields required to do business intelligence :
it adds the different levels of hierarchy on product categories and stores in the database their complete name.""",
    'author': 'Akretion',
    'website': 'http://www.akretion.com/',
    'depends': ['product'],
    'data': [],
    'installable': True,
    'active': False,
}
