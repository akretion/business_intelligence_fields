# -*- encoding: utf-8 -*-
##############################################################################
#
#    bi_sale_company_currency module for Odoo
#    Copyright (C) 2014-2015 Akretion (http://www.akretion.com/)
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

from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.one
    @api.depends(
        'order_id.pricelist_id', 'order_id.date_order', 'order_id.company_id',
        'price_unit', 'price_subtotal')
    def _compute_amount_in_company_currency(self):
        # self.order_id may be False during a small amount of time
        # (if the SO is created by code and the code create lines first
        # and then the sale.order
        price_subtotal_cc = 0.0
        price_unit_cc = 0.0
        if self.order_id and self.order_id.currency_id:
            price_subtotal_cc = self.order_id.currency_id.with_context(
                date=self.order_id.date_order,
                disable_rate_date_check=True).compute(
                    self.price_subtotal,
                    self.order_id.company_id.currency_id)
            price_unit_cc = self.order_id.currency_id.with_context(
                date=self.order_id.date_order,
                disable_rate_date_check=True).compute(
                    self.price_unit,
                    self.order_id.company_id.currency_id)
        self.price_subtotal_company_currency = price_subtotal_cc
        self.price_unit_company_currency = price_unit_cc

    price_subtotal_company_currency = fields.Float(
        compute='_compute_amount_in_company_currency',
        digits=dp.get_precision('Account'),
        string='Subtotal in Company Currency', store=True)
    price_unit_company_currency = fields.Float(
        compute='_compute_amount_in_company_currency',
        digits=dp.get_precision('Product Price'),
        string='Unit price in Company Currency', store=True)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.one
    @api.depends(
        'pricelist_id', 'date_order', 'amount_untaxed', 'amount_total',
        'company_id')
    def _compute_amount_in_company_currency(self):
        amount_untaxed_cc = 0.0
        amount_total_cc = 0.0
        if self.currency_id:
            amount_untaxed_cc = self.currency_id.with_context(
                date=self.date_order, disable_rate_date_check=True).compute(
                    self.amount_untaxed, self.company_id.currency_id)
            amount_total_cc = self.currency_id.with_context(
                date=self.date_order, disable_rate_date_check=True).compute(
                    self.amount_total, self.company_id.currency_id)
        self.amount_untaxed_company_currency = amount_untaxed_cc
        self.amount_total_company_currency = amount_total_cc

    amount_untaxed_company_currency = fields.Float(
        compute='_compute_amount_in_company_currency',
        digits=dp.get_precision('Account'),
        string='Untaxed in Company Currency', store=True)
    amount_total_company_currency = fields.Float(
        compute='_compute_amount_in_company_currency',
        digits=dp.get_precision('Account'),
        string='Total in Company Currency', store=True)
    company_currency_id = fields.Many2one(
        'res.currency', related='company_id.currency_id', readonly=True,
        string="Company Currency")
