# -*- encoding: utf-8 -*-
##############################################################################
#
#    bi_expense_company_currency module for Odoo
#    Copyright (C) 2012-2015 Akretion (http://www.akretion.com/)
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


class HrExpenseLine(models.Model):
    _inherit = "hr.expense.line"

    @api.one
    @api.depends(
        'expense_id.date_confirm', 'expense_id.company_id',
        'expense_id.currency_id', 'expense_id.account_move_id',
        'total_amount', 'amount_untaxed', 'unit_amount')
    def _compute_amount_in_company_currency(self):
        total_amount_cc = 0.0
        amount_untaxed_cc = 0.0
        unit_amount_cc = 0.0
        if self.expense_id:
            # We convert on date = date_confirm because date_confirm is the
            # date of the account move
            total_amount_cc = self.expense_id.currency_id.with_context(
                date=self.expense_id.date_confirm,
                disable_rate_date_check=True).compute(
                    self.total_amount,
                    self.expense_id.company_id.currency_id)
            amount_untaxed_cc = self.expense_id.currency_id.with_context(
                date=self.expense_id.date_confirm,
                disable_rate_date_check=True).compute(
                    self.amount_untaxed,
                    self.expense_id.company_id.currency_id)
            unit_amount_cc = self.expense_id.currency_id.with_context(
                date=self.expense_id.date_confirm,
                disable_rate_date_check=True).compute(
                    self.unit_amount,
                    self.expense_id.company_id.currency_id)
        self.total_amount_company_currency = total_amount_cc
        self.amount_untaxed_company_currency = amount_untaxed_cc
        self.unit_amount_company_currency = unit_amount_cc

    total_amount_company_currency = fields.Float(
        compute='_compute_amount_in_company_currency',
        digits=dp.get_precision('Account'),
        string='Total Amount in Company Currency', store=True)
    amount_untaxed_company_currency = fields.Float(
        compute='_compute_amount_in_company_currency',
        digits=dp.get_precision('Account'),
        string='Untaxed Amount in Company Currency', store=True)
    unit_amount_company_currency = fields.Float(
        compute='_compute_amount_in_company_currency',
        digits=dp.get_precision('Account'),
        string='Unit Price in Company Currency', store=True)


class HrExpenseExpense(models.Model):
    _inherit = 'hr.expense.expense'

    @api.one
    @api.depends(
        'date_confirm', 'company_id', 'currency_id', 'account_move_id',
        'amount', 'amount_untaxed')
    def _compute_amount_in_company_currency(self):
        self.amount_untaxed_company_currency = self.currency_id.with_context(
            date=self.date_confirm,
            disable_rate_date_check=True).compute(
                self.amount_untaxed, self.company_id.currency_id)
        self.amount_company_currency = self.currency_id.with_context(
            date=self.date_confirm,
            disable_rate_date_check=True).compute(
                self.amount, self.company_id.currency_id)

    amount_company_currency = fields.Float(
        compute='_compute_amount_in_company_currency',
        digits=dp.get_precision('Account'),
        string='Total in Company Currency', store=True)
    amount_untaxed_company_currency = fields.Float(
        compute='_compute_amount_in_company_currency',
        digits=dp.get_precision('Account'),
        string='Total Untaxed in Company Currency', store=True)
    company_currency_id = fields.Many2one(
        'res.currency', related='company_id.currency_id', readonly=True,
        string="Company Currency")
