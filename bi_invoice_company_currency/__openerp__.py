# -*- encoding: utf-8 -*-
##############################################################################
#
#    bi_invoice_company_currency module for Odoo
#    Copyright (C) 2011-2015 Akretion (http://www.akretion.com)
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
    'name': 'Business intelligence - Invoice in company currency',
    'version': '0.2',
    'summary': 'Adds fields on invoice and invoice lines for business intelligence',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'description': """
BI Invoice Company Currency
===========================

This modules adds several stored computed fields:

* on invoice line: price_subtotal_company_currency and price_unit_company_currency

* in invoice: amount_untaxed_company_currency and amount_total_company_currency

This module also replaces the object *account.invoice.report* (used by the menu entry *Reporting > Accounting > Invoice Analysis*) by another object *account.invoice.report.bi* that uses the new stored computed fields.""",
    'author': 'Akretion',
    'website': 'http://www.akretion.com/',
    'depends': ['account'],
    'data': [
        'invoice_view.xml',
        'report/invoice_report_view.xml',
        'security/ir.model.access.csv',
        ],
    'installable': True,
}
