# Copyright 2014-2021 Akretion France (http://www.akretion.com/)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends(
        'order_id.pricelist_id.currency_id',
        'order_id.date_order', 'order_id.company_id', 'price_unit',
        'price_subtotal')
    def _compute_amount_in_company_currency(self):
        for line in self:
            price_subtotal_cc = 0.0
            price_unit_cc = 0.0
            # line.order_id may be False during a small amount of time
            # (if the SO is created by code and the code create lines first
            # and then the sale.order
            order_cur = line.order_id.pricelist_id.currency_id
            if order_cur and not line.display_type:
                date = fields.Date.to_date(line.order_id.date_order)
                company = line.order_id.company_id
                company_cur = company.currency_id
                price_subtotal_cc = order_cur._convert(
                    line.price_subtotal, company_cur, company, date)
                price_unit_cc = order_cur._convert(
                    line.price_unit, company_cur, company, date)
            line.price_subtotal_company_currency = price_subtotal_cc
            line.price_unit_company_currency = price_unit_cc

    company_currency_id = fields.Many2one(
        related='order_id.company_id.currency_id',
        store=True, string='Company Currency')
    price_subtotal_company_currency = fields.Monetary(
        compute='_compute_amount_in_company_currency',
        currency_field='company_currency_id',
        string='Subtotal in Company Currency', store=True)
    price_unit_company_currency = fields.Float(
        compute='_compute_amount_in_company_currency',
        digits='Product Price',
        string='Unit price in Company Currency', store=True)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends(
        'pricelist_id.currency_id', 'date_order',
        'amount_untaxed', 'amount_total', 'company_id')
    def _compute_amount_in_company_currency(self):
        for order in self:
            amount_untaxed_cc = 0.0
            amount_total_cc = 0.0
            order_cur = order.pricelist_id.currency_id
            if order_cur:
                date = fields.Date.to_date(order.date_order)
                company = order.company_id
                company_cur = company.currency_id
                amount_untaxed_cc = order_cur._convert(
                    order.amount_untaxed, company_cur, company, date)
                amount_total_cc = order_cur._convert(
                    order.amount_total, company_cur, company, date)
            order.amount_untaxed_company_currency = amount_untaxed_cc
            order.amount_total_company_currency = amount_total_cc

    company_currency_id = fields.Many2one(
        related='company_id.currency_id', store=True,
        string="Company Currency")
    amount_untaxed_company_currency = fields.Monetary(
        compute='_compute_amount_in_company_currency',
        currency_field='company_currency_id',
        string='Untaxed in Company Currency', store=True)
    amount_total_company_currency = fields.Monetary(
        compute='_compute_amount_in_company_currency',
        currency_field='company_currency_id',
        string='Total in Company Currency', store=True)
