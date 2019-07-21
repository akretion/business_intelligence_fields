# Copyright (C) 2011-2019 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Business intelligence - Purchase Order in company currency',
    'version': '12.0.1.0.0',
    'category': 'Purchases',
    'license': 'AGPL-3',
    'summary': 'Adds fields in company currency on purchase orders and lines',
    'description': """This module adds some fields required to do business intelligence :
it adds the amount in company currency on the purchase order and purchase order lines.""",
    'author': 'Akretion',
    'website': 'http://www.akretion.com/',
    'depends': ['purchase'],
    'data': ['purchase_view.xml'],
    'installable': True,
}
