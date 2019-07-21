#  Copyright (C) 2011-2019 Akretion France (http://www.akretion.com)
#  @author Alexis de Lattre <alexis.delattre@akretion.com>
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Business intelligence - Invoice in company currency',
    'version': '12.0.1.0.0',
    'summary': 'Adds fields on invoice and invoice lines for business intelligence',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'description': """
BI Invoice Company Currency
===========================

Since Odoo v9, there are now several stored field in company currency on invoice and invoice lines. The only field in company currency lacking compared to what this module used to provide is the price unit is company currency on invoice lines. So this module now only adds that field. It also adds the fields in company currency in the view.

[NOT PORTED in v10] This module also replaces the object *account.invoice.report* (used by the menu entry *Reporting > Accounting > Invoice Analysis*) by another object *account.invoice.report.bi* that uses the new stored computed fields.""",
    'author': 'Akretion',
    'website': 'http://www.akretion.com/',
    'depends': ['account'],
    'data': [
        'invoice_view.xml',
        # 'report/invoice_report_view.xml',
        # 'security/ir.model.access.csv',
        ],
    'installable': True,
}
