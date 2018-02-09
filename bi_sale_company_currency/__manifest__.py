# -*- coding: utf-8 -*-
# Copyright (C) 2011-2018 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Business intelligence - Sale Order in company currency',
    'version': '10.0.1.0.0',
    'category': 'Sales',
    'license': 'AGPL-3',
    'summary': 'Adds fields in company currency on sale orders and lines',
    'description': """This module adds some fields required to do business intelligence :
it adds the amount in company currency on the sale order and sale order lines.""",
    'author': 'Akretion',
    'website': 'http://www.akretion.com/',
    'depends': ['sale'],
    'data': [
        'sale_view.xml',
        # The sale.report part hasn't been ported to v10 so far
        # We'll see if we need it
        # 'report/sale_report_view.xml',
        # 'security/ir.model.access.csv',
        ],
    'installable': True,
}
