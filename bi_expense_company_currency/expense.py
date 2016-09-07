# -*- encoding: utf-8 -*-
##############################################################################
#
#    bi_expense_company_currency module for OpenERP
#    Copyright (C) 2012 Akretion (http://www.akretion.com/) All Rights Reserved
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
from tools import config
import decimal_precision as dp

class hr_expense_line(osv.osv):
    _inherit = "hr.expense.line"

    def _compute_amount_in_company_currency(self, cr, uid, ids, name, arg, context=None):
        result = {}
        for exp_line in self.browse(cr, uid, ids, context=context):
            src_cur = exp_line.expense_id and exp_line.expense_id.currency_id.id or False
            company_cur = exp_line.expense_id and exp_line.expense_id.company_id.currency_id.id or False
            if src_cur and src_cur == company_cur:
                # No currency conversion required
                result[exp_line.id] = {
                    'total_amount_company_currency': exp_line.total_amount,
                    'amount_untaxed_company_currency': exp_line.amount_untaxed,
                    'unit_amount_company_currency': exp_line.unit_amount,
                }
            elif src_cur:
                # Convert on the date of the expense
                if exp_line.expense_id.date:
                    context['date'] = exp_line.expense_id.date
                    context['disable_rate_date_check'] = True
                result[exp_line.id] = {
                    'total_amount_company_currency': self.pool.get('res.currency').compute(cr, uid, src_cur, company_cur, exp_line.total_amount, context=context),
                    'amount_untaxed_company_currency': self.pool.get('res.currency').compute(cr, uid, src_cur, company_cur, exp_line.amount_untaxed, context=context),
                    'unit_amount_company_currency': self.pool.get('res.currency').compute(cr, uid, src_cur, company_cur, exp_line.unit_amount, context=context)
                }
            else:
                result[exp_line.id] = {
                    'total_amount_company_currency': False,
                    'amount_untaxed_company_currency': False,
                    'unit_amount_company_currency': False,
                }
        #print "result =", result
        return result

    def _get_expense_lines_from_expenses(self, cr, uid, ids, context=None):
        return self.pool.get('hr.expense.line').search(cr, uid, [('expense_id', 'in', ids)], context=context)

    def _get_expense_lines_from_currency_rates(self, cr, uid, ids, context=None):
        #print "_get_expense_lines_from_currency_rates IDS=", ids
        currencies_ids = self.read(cr, uid, ids, ['currency_id'], context=context)
        #print "currencies_ids=", currencies_ids
        currency_list = []
        for currency in currencies_ids:
            if currency['currency_id'][0] not in currency_list:
                currency_list.append(currency['currency_id'][0])
        #print "currency_list=", currency_list
        expense_ids = self.pool.get('hr.expense.expense').search(cr, uid, [('currency_id', 'in', currency_list)], context=context)
        #print "expense_ids =", expense_ids
        res = self.pool.get('hr.expense.line').search(cr, uid, [('expense_id', 'in', expense_ids)], context=context)
        #print "res=", res
        return res

    _columns = {
        'total_amount_company_currency': fields.function(_compute_amount_in_company_currency, multi='currencyexpline', type='float', digits_compute=dp.get_precision('Account'), string='Total amount in company currency', store={
            'hr.expense.line': (lambda self, cr, uid, ids, c={}: ids, ['unit_amount', 'unit_quantity', 'expense_id', 'product_id'], 100),
            'hr.expense.expense': (_get_expense_lines_from_expenses, ['currency_id', 'date'], 100),
            'res.currency.rate': (_get_expense_lines_from_currency_rates, ['name', 'rate', 'currency_id'], 100),
            }),
        'amount_untaxed_company_currency': fields.function(_compute_amount_in_company_currency, multi='currencyexpline', type='float', digits_compute=dp.get_precision('Account'), string='Total untaxed in company currency', store={
            'hr.expense.line': (lambda self, cr, uid, ids, c={}: ids, ['unit_amount', 'unit_quantity', 'expense_id', 'product_id'], 100),
            'hr.expense.expense': (_get_expense_lines_from_expenses, ['currency_id', 'date'], 100),
            'res.currency.rate': (_get_expense_lines_from_currency_rates, ['name', 'rate', 'currency_id'], 100),
            }),
        'unit_amount_company_currency': fields.function(_compute_amount_in_company_currency, multi='currencyexpline', type='float', digits_compute=dp.get_precision('Account'), string='Unit price in company currency', store={
            'hr.expense.line': (lambda self, cr, uid, ids, c={}: ids, ['unit_amount', 'expense_id', 'product_id'], 100),
            'hr.expense.expense': (_get_expense_lines_from_expenses, ['currency_id', 'date'], 100),
            'res.currency.rate': (_get_expense_lines_from_currency_rates, ['name', 'rate', 'currency_id'], 100),
            }),
    }
