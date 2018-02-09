# -*- coding: utf-8 -*-
# Copyright (C) 2011-2018 Akretion (http://www.akretion.com/)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


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
    @api.depends(
        'invoice_id.currency_id', 'invoice_id.move_id',
        'invoice_id.date_invoice', 'invoice_id.company_id', 'price_unit')
    def _compute_amount_in_company_currency(self):
        for line in self:
            price_unit_cc = 0.0
            if line.invoice_id:
                # Convert on the date of the invoice
                price_unit_cc = line.invoice_id.currency_id.with_context(
                    date=line.invoice_id.date_invoice,
                    disable_rate_date_check=True).compute(
                        line.price_unit,
                        line.invoice_id.company_id.currency_id)
            line.price_unit_company_currency = price_unit_cc

    company_currency_id = fields.Many2one(store=True)
    # in v10, our former field 'price_subtotal_company_currency'
    # has a native equivalent: price_subtotal_signed
    price_unit_company_currency = fields.Float(
        compute='_compute_amount_in_company_currency',
        digits=dp.get_precision('Product Price'),
        string='Unit Price in Company Currency', store=True, readonly=True)


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    # in v10, our former field 'amount_untaxed_company_currency'
    # has a native equivalent: amount_untaxed_signed
    # which is in company cur. (even if the field name doesn't reflect that)
    # in v10, our former field 'amount_total_company_currency'
    # has a native equivalent: amount_total_company_signed
    company_currency_id = fields.Many2one(store=True)
