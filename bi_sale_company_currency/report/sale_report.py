# -*- coding: utf-8 -*-
##############################################################################
#
#    bi_sale_company_currency module for Odoo
#    Copyright (C) 2016 Akretion (http://www.akretion.com/)
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


class SaleReportBi(models.Model):
    _name = "sale.report.bi"
    _description = "Sales Statistics"
    _auto = False
    _rec_name = 'date_confirm'

    date_confirm = fields.Date(string='Date Confirm', readonly=True)
    sale_number = fields.Char(string='Sale Order Number', readonly=True)
    product_id = fields.Many2one(
        'product.product', string='Product', readonly=True)
    product_uom_qty = fields.Float(string='Product Quantity', readonly=True)
    amount_company_currency = fields.Float(
        string='Amount Without Tax', readonly=True,
        digits=dp.get_precision('Account'))
    # TODO : add support for UoM and UoM conversion ?
    # uom_name = fields.Char(
    #    string='Reference Unit of Measure', size=128, readonly=True)
    payment_term_id = fields.Many2one(
        'account.payment.term', string='Payment Term', readonly=True)
    fiscal_position_id = fields.Many2one(
        'account.fiscal.position', string='Fiscal Position', readonly=True)
    pricelist_id = fields.Many2one(
        'product.pricelist', string='Pricelist', readonly=True)
    categ_id = fields.Many2one(
        'product.category', string='Category of Product', readonly=True)
    # I put only the field commercial_partner_id to avoid confusing the users
    # with 2 fields partner_id and commercial_partner_id
    commercial_partner_id = fields.Many2one(
        'res.partner', string='Customer', readonly=True)
    company_id = fields.Many2one(
        'res.company', string='Company', readonly=True)
    user_id = fields.Many2one(
        'res.users', string='Salesperson', readonly=True)
    state = fields.Selection([
        ('cancel', 'Cancelled'),
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('exception', 'Exception'),
        ('done', 'Done'),
        ], string='Order Status', readonly=True)
    country_id = fields.Many2one(
        'res.country', string='Country of the Customer', readonly=True)
    section_id = fields.Many2one(
        'crm.case.section', string='Sales Team', readonly=True)
    analytic_account_id = fields.Many2one(
        'account.analytic.account', string='Analytic Account', readonly=True)

    _order = 'date_confirm desc'
    _depends = {
        'sale.order': [
            'partner_id',
            'company_id', 'pricelist_id', 'date_confirm',
            'fiscal_position', 'partner_id', 'payment_term',
            'state', 'user_id', 'name', 'section_id', 'project_id',
        ],
        'sale.order.line': [
            'order_id', 'price_subtotal', 'product_id',
            'product_uom_qty', 'product_uom',
        ],
        'product.product': ['product_tmpl_id'],
        'product.template': ['categ_id'],
        # 'product.uom': ['category_id', 'factor', 'name', 'uom_type'],
        'res.partner': ['country_id', 'commercial_partner_id'],
    }

    # TODO : check that the sum works on quantity with refunds
    def _select(self):
        select = """
        SELECT min(sol.id) AS id,
        so.date_confirm AS date_confirm,
        so.name AS sale_number,
        sol.product_id AS product_id,
        sum(sol.product_uom_qty) AS product_uom_qty,
        so.payment_term AS payment_term_id,
        so.fiscal_position AS fiscal_position_id,
        pt.categ_id AS categ_id,
        rp.commercial_partner_id AS commercial_partner_id,
        so.company_id AS company_id,
        so.user_id AS user_id,
        sum(sol.price_subtotal_company_currency) AS amount_company_currency,
        so.state AS state,
        so.pricelist_id AS pricelist_id,
        so.section_id AS section_id,
        so.project_id AS analytic_account_id,
        crp.country_id AS country_id
        """
        return select

    def _from(self):
        from_sql = """
        sale_order_line sol
            LEFT JOIN sale_order so ON sol.order_id = so.id
            LEFT JOIN product_product pp ON sol.product_id=pp.id
            LEFT JOIN product_template pt ON pp.product_tmpl_id=pt.id
            LEFT JOIN res_partner rp ON rp.id = so.partner_id
            LEFT JOIN res_partner crp ON rp.commercial_partner_id = crp.id
        """
        return from_sql

    def _where(self):
        where = """
        WHERE so.state not in ('draft', 'sent', 'cancel')
        """
        return where

    def _group_by(self):
        group_by = """
        GROUP BY so.date_confirm, so.name, sol.product_id,
        so.payment_term, so.fiscal_position, pt.categ_id,
        rp.commercial_partner_id, so.company_id, so.user_id,
        so.state, so.pricelist_id, so.section_id, so.project_id,
        crp.country_id
        """
        return group_by

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("CREATE or REPLACE VIEW %s as (%s FROM %s %s %s)" % (
            self._table, self._select(), self._from(), self._where(),
            self._group_by()))
