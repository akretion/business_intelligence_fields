# -*- encoding: utf-8 -*-
##############################################################################
#
#    bi_purchase_company_currency module for OpenERP
#    Copyright (C) 2014 Akretion (http://www.akretion.com/)
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
import openerp.addons.decimal_precision as dp


class purchase_order_line(orm.Model):
    _inherit = "purchase.order.line"

    def _compute_amount_in_company_currency(
            self, cr, uid, ids, name, arg, context=None):
        if context is None:
            context = {}
        result = {}
        for po_line in self.browse(cr, uid, ids, context=context):
            src_cur = (
                po_line.order_id and po_line.order_id.currency_id.id
                or False)
            company_cur = (
                po_line.order_id and
                po_line.order_id.company_id.currency_id.id or False)
            # We need to test if src_cur exists, because po_line.order_id
            # may be False during a small amount (if the SO is created by
            # code and the code create lines first and then the order
            if src_cur and src_cur == company_cur:
                # No currency conversion required
                result[po_line.id] = {
                    'price_subtotal_company_currency': po_line.price_subtotal,
                    'price_unit_company_currency': po_line.price_unit,
                }
            elif src_cur:
                # Convert on the date of the order
                cc_ctx = context.copy()
                if po_line.order_id.date_order:
                    cc_ctx['date'] = po_line.order_id.date_order
                result[po_line.id] = {
                    'price_subtotal_company_currency':
                    self.pool['res.currency'].compute(
                        cr, uid, src_cur, company_cur,
                        po_line.price_subtotal, context=cc_ctx),
                    'price_unit_company_currency':
                    self.pool['res.currency'].compute(
                        cr, uid, src_cur, company_cur,
                        po_line.price_unit, context=cc_ctx)
                }
            else:
                result[po_line.id] = {
                    'price_subtotal_company_currency': False,
                    'price_unit_company_currency': False,
                }
        #print "result =", result
        return result

    def _get_polines_from_orders(self, cr, uid, ids, context=None):
        return self.pool['purchase.order.line'].search(
            cr, uid, [('order_id', 'in', ids)], context=context)

    _columns = {
        'price_subtotal_company_currency': fields.function(
            _compute_amount_in_company_currency, multi='currencypoline',
            type='float', digits_compute=dp.get_precision('Account'),
            string='Subtotal in Company Currency', store={
                'purchase.order.line': (
                    lambda self, cr, uid, ids, c={}: ids,
                    ['price_unit', 'product_qty', 'order_id', 'tax_id'],
                    100),
                'purchase.order': (
                    _get_polines_from_orders, ['date_order', 'pricelist_id'],
                    100),
            }),
        'price_unit_company_currency': fields.function(
            _compute_amount_in_company_currency, multi='currencypoline',
            type='float', digits_compute=dp.get_precision('Product Price'),
            string='Unit price in Company Currency', store={
                'purchase.order.line': (
                    lambda self, cr, uid, ids, c={}: ids,
                    ['price_unit', 'order_id'], 100),
                'purchase.order': (
                    _get_polines_from_orders, ['date_order', 'pricelist_id'],
                    100),
                }),
    }


class purchase_order(orm.Model):
    _inherit = "purchase.order"

    def _compute_amount_in_company_currency(
            self, cr, uid, ids, name, arg, context=None):
        if context is None:
            context = {}
        result = {}
        for so in self.browse(cr, uid, ids, context=context):
            if so.currency_id == so.company_id.currency_id:
                # No currency conversion required
                result[so.id] = {
                    'amount_untaxed_company_currency': so.amount_untaxed,
                    'amount_total_company_currency': so.amount_total,
                }
            else:
                # Convert on the date of the SO
                cc_ctx = context.copy()
                if so.date_order:
                    cc_ctx['date'] = so.date_order
                result[so.id] = {
                    'amount_untaxed_company_currency':
                    self.pool['res.currency'].compute(
                        cr, uid, so.currency_id.id,
                        so.company_id.currency_id.id, so.amount_untaxed,
                        context=cc_ctx),
                    'amount_total_company_currency':
                    self.pool['res.currency'].compute(
                        cr, uid, so.currency_id.id,
                        so.company_id.currency_id.id, so.amount_total,
                        context=cc_ctx)
                }
        #print "result =", result
        return result

    def _bi_get_purchase_order_line(self, cr, uid, ids, context=None):
        return self.pool['purchase.order']._get_order(
            cr, uid, ids, context=context)

    _columns = {
        'amount_untaxed_company_currency': fields.function(
            _compute_amount_in_company_currency, multi='currencypo',
            type='float', digits_compute=dp.get_precision('Account'),
            string='Untaxed in Company Currency', store={
                'purchase.order': (
                    lambda self, cr, uid, ids, c={}: ids,
                    ['order_line', 'date_order', 'pricelist_id'], 100),
                'purchase.order.line': (
                    _bi_get_purchase_order_line, [
                        'price_unit',
                        'tax_id',
                        'product_uom_qty',
                        'discount',
                        'order_id'], 100),
            }),
        'amount_total_company_currency': fields.function(
            _compute_amount_in_company_currency, multi='currencypo',
            type='float', digits_compute=dp.get_precision('Account'),
            string='Total in Company Currency', store={
                'purchase.order': (
                    lambda self, cr, uid, ids, c={}:
                    ids, ['order_line', 'date_order', 'pricelist_id'], 100),
                'purchase.order.line': (
                    _bi_get_purchase_order_line, [
                        'price_unit',
                        'taxes_id',
                        'product_qty',
                        'order_id',
                        ], 100),
            }),
        'company_currency_id': fields.related(
            'company_id', 'currency_id', readonly=True, type='many2one',
            relation='res.currency', string="Company Currency"),
    }
