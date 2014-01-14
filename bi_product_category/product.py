# -*- encoding: utf-8 -*-
##############################################################################
#
#    bi_product_category module for OpenERP
#    Copyright (C) 2013-2014 Akretion (http://www.akretion.com/)
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


class product_category(orm.Model):
    _inherit = "product.category"

    def _invalidate_categ(self, cr, uid, ids, context=None):
        # We need to invalidate the categ itself
        # + its childrens of all generations
        res = []
        for categ in self.browse(cr, uid, ids, context=context):
            if categ.id not in res:
                res.append(categ.id)
            # To understand parent_left and parent_right
            # https://answers.launchpad.net/openobject-server/+question/186704
            cr.execute(
                'SELECT id FROM product_category WHERE parent_left > %s '
                'AND parent_right < %s',
                (categ.parent_left, categ.parent_right))
            all_gen_childs_res = cr.fetchall()
            for child_item in all_gen_childs_res:
                if (child_item and isinstance(child_item[0], int)
                        and child_item[0] not in res):
                    res.append(child_item[0])
        return res

    def _compute_layers_name(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for categ in self.read(
                cr, uid, ids, ['name', 'parent_id'], context=context):
            # We can't read the 'complete_name' and split it,
            # because the complete_name doesn't have it's new value yet
            reverse_hierachy = [categ['name']]
            parent_id = categ['parent_id'] and categ['parent_id'][0] or False
            while parent_id:
                parent_categ = self.read(
                    cr, uid, parent_id, ['name', 'parent_id'], context=context)
                reverse_hierachy.append(parent_categ['name'])
                parent_id = parent_categ['parent_id'] and \
                    parent_categ['parent_id'][0] or False

            res[categ['id']] = {
                'bi_l1_name':
                reverse_hierachy and reverse_hierachy[-1] or 'None',
                'bi_l2_name':
                len(reverse_hierachy) >= 2 and reverse_hierachy[-2] or 'None',
                'bi_l3_name':
                len(reverse_hierachy) >= 3 and reverse_hierachy[-3] or 'None',
                'bi_l4_name':
                len(reverse_hierachy) >= 4 and reverse_hierachy[-4] or 'None',
                'bi_l5_name':
                len(reverse_hierachy) >= 5 and reverse_hierachy[-5] or 'None',
                'bi_l6_name':
                len(reverse_hierachy) >= 6 and reverse_hierachy[-6] or 'None',
            }
        return res

    def _bi_name_get_fnc(self, cr, uid, ids, name, arg, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)

    _columns = {
        # Inherit this field to make it a store field
        'complete_name': fields.function(
            _bi_name_get_fnc, type="char", size=500, string='Name', store={
                'product.category': (
                    _invalidate_categ, ['name', 'parent_id'], 10),
            }),
        'bi_l1_name': fields.function(
            _compute_layers_name, type='char', size=64, multi='layers',
            string='Layer 1 name', store={
                'product.category': (
                    _invalidate_categ, ['name', 'parent_id'], 10),
            }),
        'bi_l2_name': fields.function(
            _compute_layers_name, type='char', size=64, multi='layers',
            string='Layer 2 name', store={
                'product.category': (
                    _invalidate_categ, ['name', 'parent_id'], 10),
            }),
        'bi_l3_name': fields.function(
            _compute_layers_name, type='char', size=64, multi='layers',
            string='Layer 3 name', store={
                'product.category': (
                    _invalidate_categ, ['name', 'parent_id'], 10),
            }),
        'bi_l4_name': fields.function(
            _compute_layers_name, type='char', size=64, multi='layers',
            string='Layer 4 name', store={
                'product.category': (
                    _invalidate_categ, ['name', 'parent_id'], 10),
            }),
        'bi_l5_name': fields.function(
            _compute_layers_name, type='char', size=64, multi='layers',
            string='Layer 5 name', store={
                'product.category': (
                    _invalidate_categ, ['name', 'parent_id'], 10),
            }),
        'bi_l6_name': fields.function(
            _compute_layers_name, type='char', size=64, multi='layers',
            string='Layer 6 name', store={
                'product.category': (
                    _invalidate_categ, ['name', 'parent_id'], 10),
            }),
        }
