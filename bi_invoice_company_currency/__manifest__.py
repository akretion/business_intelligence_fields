#  Copyright 2011-2021 Akretion France (http://www.akretion.com)
#  @author Alexis de Lattre <alexis.delattre@akretion.com>
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Invoice in company currency',
    'version': '14.0.1.0.0',
    'summary': 'Adds price unit in company currency on invoice lines',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'description': """
BI Invoice Company Currency
===========================

This module adds a field **price_unit_company_currency** on move lines.
""",
    'author': 'Akretion',
    'website': 'http://www.akretion.com/',
    'depends': ['account'],
    'installable': True,
}
