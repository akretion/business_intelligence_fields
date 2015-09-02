# -*- encoding: utf-8 -*-
##############################################################################
#
#    bi_invoice_company_currency module for Odoo
#    Copyright (C) 2011-2015 Akretion (http://www.akretion.com/)
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


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    # In @api.depends, why do I have accout.invoice -> move_id, and not
    # 'res.currency.rate' ? Answer : because, in the accounting
    # entries, the computation of currency conversion takes place
    # when the accountings entries are created, i.e. when the
    # invoice goes from 'draft' to 'open'. It is not re-computed
    # every time a new currency rate is entered. So we want to
    # compute the currency conversion simultaneously with the
    # accounting entries. That's why we trigger on move_id field on
    # account.invoice.
    @api.one
    @api.depends(
        'invoice_id.currency_id', 'invoice_id.move_id',
        'invoice_id.date_invoice', 'invoice_id.type', 'invoice_id.company_id',
        'price_subtotal', 'price_unit')
    def _compute_amount_in_company_currency(self):
        price_subtotal_cc = 0.0
        price_unit_cc = 0.0
        sign = 1
        if self.invoice_id:
            if self.invoice_id.type in ('out_refund', 'in_refund'):
                sign = -1
            # Convert on the date of the invoice
            price_subtotal_cc = self.invoice_id.currency_id.with_context(
                date=self.invoice_id.date_invoice,
                disable_rate_date_check=True).compute(
                    self.price_subtotal,
                    self.invoice_id.company_id.currency_id) * sign
            price_unit_cc = self.invoice_id.currency_id.with_context(
                date=self.invoice_id.date_invoice,
                disable_rate_date_check=True).compute(
                    self.price_unit,
                    self.invoice_id.company_id.currency_id)
        self.price_subtotal_company_currency = price_subtotal_cc
        self.price_unit_company_currency = price_unit_cc

    price_subtotal_company_currency = fields.Float(
        compute='_compute_amount_in_company_currency',
        digits=dp.get_precision('Account'),
        string='Subtotal in Company Currency', store=True,
        help='The amount is negative for a refund')
    price_unit_company_currency = fields.Float(
        compute='_compute_amount_in_company_currency',
        digits=dp.get_precision('Account'),
        string='Unit Price in Company Currency', store=True)


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.one
    @api.depends(
        'currency_id', 'move_id', 'date_invoice', 'type', 'company_id',
        'amount_untaxed', 'amount_total')
    def _compute_amount_in_company_currency(self):
        # Convert on the date of the invoice
        sign = 1
        if self.type in ('out_refund', 'in_refund'):
            sign = -1
        self.amount_untaxed_company_currency = self.currency_id.with_context(
            date=self.date_invoice, disable_rate_date_check=True).compute(
                self.amount_untaxed, self.company_id.currency_id) * sign
        self.amount_total_company_currency = self.currency_id.with_context(
            date=self.date_invoice, disable_rate_date_check=True).compute(
                self.amount_total, self.company_id.currency_id) * sign

    amount_untaxed_company_currency = fields.Float(
        compute='_compute_amount_in_company_currency',
        digits=dp.get_precision('Account'),
        string='Total Untaxed in Company Currency', store=True,
        help='The amount is negative for a refund')
    amount_total_company_currency = fields.Float(
        compute='_compute_amount_in_company_currency',
        digits=dp.get_precision('Account'),
        string='Total in Company Currency', store=True,
        help='The amount is negative for a refund')
    company_currency_id = fields.Many2one(
        'res.currency', related='company_id.currency_id', readonly=True,
        string="Company Currency")
