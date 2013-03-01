# -*- encoding: utf-8 -*-
##############################################################################
#
#    bi_partner module for OpenERP
#    Copyright (C) 2013 Akretion (http://www.akretion.com). All Rights Reserved
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

from osv import osv, fields

class res_partner(osv.osv):
    _inherit = "res.partner"

    def get_partner_from_address(self, cr, uid, ids, context=None):
        res = []
        for partner_address_id in ids:
            partner = self.read(cr, uid, partner_address_id, ['partner_id'], context=context)['partner_id']
            if partner and partner[0] not in res:
                res.append(partner[0])
        return res


    _columns = {
        'country': fields.related('address', 'country_id', type='many2one', relation='res.country', string='Country', store={
            'res.partner.address': (get_partner_from_address, ['partner_id', 'country_id'], 10)
        }),
    }

