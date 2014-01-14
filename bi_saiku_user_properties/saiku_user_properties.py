# -*- coding: utf-8 -*-
##############################################################################
#
#    bi_saiku_user_properties module for OpenERP
#    Copyright (C) 2014 Akretion (http://www.akretion.com)
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

from openerp.osv import orm, fields
from openerp import SUPERUSER_ID
import logging

logger = logging.getLogger(__name__)


class saiku_user_properties(orm.Model):
    _name = "saiku.user.properties"
    _columns = {
        'saiku_user_properties_file': fields.property(
            None, type='char', size=300,
            string='Full Path to Saiku User Properties'),
    }

    def _generate_saiku_user_properties(self, cr, uid, context=None):
        res_bi_group = self.pool['ir.model.data'].get_object_reference(
            cr, uid, 'bi_saiku_user_properties',
            'group_business_intelligence')
        if res_bi_group and res_bi_group[0] == 'res.groups':
            bi_group_id = res_bi_group[1]
        else:
            raise orm.except_orm('Error', 'This should never happen')
        bi_user_ids = self.pool['res.groups'].read(
            cr, uid, bi_group_id, ['users'], context=context)['users']
        if bi_user_ids:
            user_prop = u'#This file is auto-generated and kept up-to-date'\
                + u' by OpenERP\n#Username,password,role\n'
            for user in self.pool['res.users'].browse(
                    cr, uid, bi_user_ids, context=context):
                user_prop += u'%s=%s,ROLE_USER' % (user.login, user.password)
                if user.id == SUPERUSER_ID:
                    user_prop += u',ROLE_ADMIN'
                user_prop += u'\n'
            user_properties_file = self.pool['ir.property'].get(
                cr, uid, 'saiku_user_properties_file',
                'saiku.user.properties', context=context)
            if not user_properties_file:
                raise orm.except_orm(
                    'Error:',
                    "No value for property 'Full Path to Saiku User "
                    "Properties'")
            user_file = open(user_properties_file, 'wb')
            user_file.seek(0)
            user_file.write(user_prop)
            user_file.close()
            logger.info(
                "Saiku file '%s' updated"
                % user_properties_file)
        else:
            logger.info('There are no Business Intelligence users in OpenERP')
        return True
