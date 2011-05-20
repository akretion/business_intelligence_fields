# -*- encoding: utf-8 -*-
##############################################################################
#
#    Business Intelligence fields module for OpenERP
#    Copyright (C) 2011 Akretion (http://www.akretion.com/) All Rights Reserved
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

class account_invoice_line(osv.osv):
    _inherit = "account.invoice.line"

    def _compute_amount_in_company_currency(self, cr, uid, ids, name, arg, context=None):
        result = {}
        for inv_line in self.browse(cr, uid, ids, context=context):
            if inv_line.invoice_id.currency_id == inv_line.invoice_id.company_id.currency_id:
                # No currency conversion required
                result[inv_line.id] = {
                    'price_subtotal_company_currency': inv_line.price_subtotal,
                    'price_unit_company_currency': inv_line.price_unit,
                }
            else:
                # Convert on the date of the invoice
                if inv_line.invoice_id.date_invoice:
                    context['date'] = inv_line.invoice_id.date_invoice
                result[inv_line.id] = {
                    'price_subtotal_company_currency': self.pool.get('res.currency').compute(cr, uid, inv_line.invoice_id.currency_id.id, inv_line.invoice_id.company_id.currency_id.id, inv_line.price_subtotal, context=context),
                    'price_unit_company_currency': self.pool.get('res.currency').compute(cr, uid, inv_line.invoice_id.currency_id.id, inv_line.invoice_id.company_id.currency_id.id, inv_line.price_unit, context=context)
                }
        #print "result =", result
        return result

    def _get_invoice_lines_from_invoices(self, cr, uid, ids, context=None):
        return self.pool.get('account.invoice.line').search(cr, uid, [('invoice_id', 'in', ids)], context=context)

    _columns = {
        'price_subtotal_company_currency': fields.function(_compute_amount_in_company_currency, method=True, multi='currencyconvert', type='float', digits=(16, int(config['price_accuracy'])), string='Subtotal in company currency', store={
            'account.invoice.line': (lambda self, cr, uid, ids, c={}: ids, ['price_subtotal'], 10),
            'account.invoice': (_get_invoice_lines_from_invoices, ['move_id'], 20),
            }),
        # In the trigger object for invalidation of these function fields,
        # why do I have accout.invoice -> move_id, and not 'res.currency.rate' ?
        # Answer : because, in the accounting entries, the computation of currency conversion
        # takes place when the accountings entries are created, i.e. when the invoice goes
        # from 'draft' to 'open'. It is not re-computed every time a new currency rate is
        # entered. So we want to compute the currency conversion simultaneously with the
        # accounting entries. That's why we trigger on move_id field on account.invoice.
        'price_unit_company_currency': fields.function(_compute_amount_in_company_currency, method=True, multi='currencyconvert', type='float', digits=(16, int(config['price_accuracy'])), string='Unit price in company currency', store={
            'account.invoice.line': (lambda self, cr, uid, ids, c={}: ids, ['price_unit'], 10),
            'account.invoice': (_get_invoice_lines_from_invoices, ['move_id'], 20),

            }),
    }

account_invoice_line()

