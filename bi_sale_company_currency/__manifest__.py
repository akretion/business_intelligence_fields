# Copyright 2011-2021 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Order in company currency',
    'version': '14.0.1.0.0',
    'category': 'Sales',
    'license': 'AGPL-3',
    'summary': 'Adds fields in company currency on sale orders and sale order lines',
    'description': """This module adds some fields required to do business intelligence :
it adds the amount in company currency on the sale order and sale order lines.""",
    'author': 'Akretion',
    'website': 'http://www.akretion.com/',
    'depends': ['sale'],
    'data': [
        'views/sale_order.xml',
        ],
    'installable': True,
}
