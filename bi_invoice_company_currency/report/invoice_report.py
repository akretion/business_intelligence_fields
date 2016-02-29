# -*- coding: utf-8 -*-
##############################################################################
#
#    bi_invoice_company_currency module for Odoo
#    Copyright (C) 2015 Akretion (http://www.akretion.com/)
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

from openerp import models, fields, tools
import openerp.addons.decimal_precision as dp


class AccountInvoiceReportBi(models.Model):
    _name = "account.invoice.report.bi"
    _description = "Invoices Statistics"
    _auto = False
    _rec_name = 'date_invoice'

    date_invoice = fields.Date(string='Date', readonly=True)
    invoice_number = fields.Char(string='Invoice Number', readonly=True)
    product_id = fields.Many2one(
        'product.product', string='Product', readonly=True)
    product_qty = fields.Float(string='Product Quantity', readonly=True)
    amount_company_currency = fields.Float(
        string='Amount Without Tax', readonly=True,
        digits=dp.get_precision('Account'))
    uom_id = fields.Many2one(
        'product.uom', string='Unit of Measure', readonly=True,
        help="Unit of measure of the product (may be different from the "
        "unit of measure used in some invoice lines)")
    payment_term = fields.Many2one(
        'account.payment.term', string='Payment Term', readonly=True)
    period_id = fields.Many2one(
        'account.period', string='Period', readonly=True)
    fiscal_position = fields.Many2one(
        'account.fiscal.position', string='Fiscal Position', readonly=True)
    currency_id = fields.Many2one(
        'res.currency', string='Currency', readonly=True)
    categ_id = fields.Many2one(
        'product.category', 'Category of Product', readonly=True)
    journal_id = fields.Many2one(
        'account.journal', string='Journal', readonly=True)
    # I put only the field commercial_partner_id to avoid confusing the users
    # with 2 fields partner_id and commercial_partner_id
    commercial_partner_id = fields.Many2one(
        'res.partner', 'Partner Company', help="Commercial Entity")
    company_id = fields.Many2one(
        'res.company', string='Company', readonly=True)
    user_id = fields.Many2one(
        'res.users', 'Salesperson', readonly=True)
    type = fields.Selection([
        ('out_invoice', 'Customer Invoice'),
        ('in_invoice', 'Supplier Invoice'),
        ('out_refund', 'Customer Refund'),
        ('in_refund', 'Supplier Refund'),
        ], string='Type', readonly=True)
    state = fields.Selection([
        ('open', 'Open'),
        ('paid', 'Paid'),
        ], string='Invoice Status', readonly=True)
    date_due = fields.Date(string='Due Date', readonly=True)
    account_line_id = fields.Many2one(
        'account.account', string='Account Line', readonly=True)
    country_id = fields.Many2one(
        'res.country', string='Country of the Partner Company')

    _order = 'date_invoice desc'
    _depends = {
        'account.invoice': [
            'account_id', 'amount_total', 'commercial_partner_id',
            'company_id', 'currency_id', 'date_due', 'date_invoice',
            'fiscal_position', 'journal_id', 'partner_id', 'payment_term',
            'period_id', 'state', 'type', 'user_id', 'number',
        ],
        'account.invoice.line': [
            'account_id', 'invoice_id', 'price_subtotal', 'product_id',
            'quantity', 'uos_id',
        ],
        'product.product': ['product_tmpl_id'],
        'product.template': ['categ_id'],
        'product.uom': ['category_id', 'factor', 'name', 'uom_type'],
        'res.partner': ['country_id'],
    }

    def _select(self):
        select = """
        SELECT min(ail.id) AS id,
        ai.date_invoice AS date_invoice,
        ai.number AS invoice_number,
        ail.product_id AS product_id,
        sum(CASE WHEN ai.type IN ('out_refund', 'in_refund')
            THEN - ail.quantity * uom_product.factor / uom_inv.factor
            ELSE ail.quantity * uom_product.factor / uom_inv.factor
            END)
        AS product_qty,
        pt.uom_id AS uom_id,
        ai.payment_term AS payment_term,
        ai.period_id AS period_id,
        ai.fiscal_position AS fiscal_position,
        ai.currency_id AS currency_id,
        pt.categ_id AS categ_id,
        ai.journal_id AS journal_id,
        ai.commercial_partner_id AS commercial_partner_id,
        ai.company_id AS company_id,
        ai.user_id AS user_id,
        sum(ail.price_subtotal_company_currency) AS amount_company_currency,
        ai.type AS type,
        ai.state AS state,
        ai.date_due AS date_due,
        ail.account_id AS account_line_id,
        rp.country_id AS country_id
        """
        return select

    def _from(self):
        from_sql = """
        account_invoice_line ail
            LEFT JOIN account_invoice ai ON ail.invoice_id = ai.id
            LEFT JOIN product_product pp ON ail.product_id=pp.id
            LEFT JOIN product_template pt ON pp.product_tmpl_id=pt.id
            LEFT JOIN res_partner rp ON rp.id = ai.commercial_partner_id
            LEFT JOIN product_uom uom_inv ON uom_inv.id = ail.uos_id
            LEFT JOIN product_uom uom_product ON uom_product.id = pt.uom_id
        """
        return from_sql

    def _where(self):
        where = """WHERE ai.state in ('open', 'paid')"""
        return where

    def _group_by(self):
        group_by = """
        GROUP BY ai.date_invoice, ai.number, ail.product_id, ai.payment_term,
        ai.period_id, ai.fiscal_position, ai.currency_id, pt.categ_id,
        ai.journal_id, ai.commercial_partner_id, ai.company_id, ai.user_id,
        ai.type, ai.state, ai.date_due, ail.account_id, rp.country_id,
        pt.uom_id
        """
        return group_by

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("CREATE or REPLACE VIEW %s as (%s FROM %s %s %s)" % (
            self._table, self._select(), self._from(), self._where(),
            self._group_by()))
