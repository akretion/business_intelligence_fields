# -*- coding: utf-8 -*-
# Copyright (C) 2013-2018 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Business intelligence - Time dimension',
    'summary': 'Generate time dimension table for BI',
    'version': '10.0.1.0.0',
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
    'installable': True,
}
