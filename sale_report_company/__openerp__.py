# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Business Applications
#    Copyright (c) 2013 OpenERP S.A. <http://openerp.com>
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
    'name': 'Sales Consolidation per Customer Company',
    'version': '1.0',
    'category': 'Hidden/Dependency',
    'description': """
Add an extra Customer Company dimension on Quotations/Orders lists
==================================================================

By Quotations and Sales Orders can be associated with any given Customer
or any Customer Contact. When using contacts, the company these contacts
belong to is not directly available as a grouping dimension in
Quotations and Sales Orders lists.
This modules adds an extra "group by" dimension labelled "Customer Company".

For B2C where the Customer is a natural person, the Customer Company
value will be that person herself. 

Note: this module will likely be removed in OpenERP 8.0, and may be
directly integrated in the core Sales Management module. 
""",
    'author': 'OpenERP SA',
    'website': 'http://www.openerp.com',
    'depends': ['sale'],
    'data': [
        'sale_view.xml',
    ],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
