# -*- encoding: utf-8 -*-
##############################################################################
#
#    bi_saiku_user_properties module for OpenERP
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
    'name': 'Business Intelligence - Saiku User Properties',
    'version': '0.1',
    'category': 'Business Intelligence',
    'license': 'AGPL-3',
    'description': """This module generates the user.properties file of Saiku from the OpenERP login and passwords.

Please contact Alexis de Lattre from Akretion <alexis.delattre@akretion.com> for any help or question about this module.
""",
    'author': 'Akretion',
    'website': 'http://www.akretion.com/',
    'depends': ['base'],
    'data': [
        'security/bi_group.xml',
        'saiku_user_properties_cron.xml',
        'saiku_user_properties_data.xml',
        ],
    'installable': True,
    'active': False,
}
