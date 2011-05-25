# -*- encoding: utf-8 -*-
##############################################################################
#
#    bi_invoice_payment module for OpenERP
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

class account_invoice(osv.osv):
    _inherit = "account.invoice"

    def _compute_bi_payment(self, cr, uid, ids, name, arg, context=None):
        result = {}
        for inv in self.browse(cr, uid, ids, context=context):
            date_final_payment_to_write = False
            max_date_all_journals = False
            max_date_cash_journal = False
            total_down_pay_to_write = 0.0
            total_down_pay = 0.0
            for payment in inv.payment_ids:
                if payment.date and payment.date > max_date_all_journals:
                    max_date_all_journals = payment.date
                if payment.date and payment.journal_id and payment.journal_id.type == 'cash' and payment.date > max_date_cash_journal:
                    max_date_cash_journal = payment.date

                if payment.date < inv.date_invoice:
                    total_down_pay += payment.credit - payment.debit

            if inv.type in ('in_invoice', 'out_invoice'):
                if inv.reconciled:
                    if max_date_cash_journal:
                        date_final_payment_to_write = max_date_cash_journal
                    elif max_date_all_journals:
                        date_final_payment_to_write = max_date_all_journals

                total_down_pay_to_write = total_down_pay


            result[inv.id] = {
                    'date_final_payment': date_final_payment_to_write,
                    'total_down_payment_company_currency': total_down_pay_to_write,
            }
        print "result =", result
        return result

    def _bi_get_invoice_line(self, cr, uid, ids, context=None):
        return self.pool.get('account.invoice')._get_invoice_line(cr, uid, ids, context=context)

    def _bi_get_invoice_tax(self, cr, uid, ids, context=None):
        return self.pool.get('account.invoice')._get_invoice_tax(cr, uid, ids, context=context)

    def _bi_get_invoice_from_line(self, cr, uid, ids, context=None):
        return self.pool.get('account.invoice')._get_invoice_from_line(cr, uid, ids, context=context)

    def _bi_get_invoice_from_reconcile(self, cr, uid, ids, context=None):
        return self.pool.get('account.invoice')._get_invoice_from_reconcile(cr, uid, ids, context=context)

    _columns = {
        'date_final_payment': fields.function(_compute_bi_payment, method=True, multi='bipay', type='date', string='Final payment date', store={
            'account.move.line': (_bi_get_invoice_from_line, None, 50),
            'account.move.reconcile': (_bi_get_invoice_from_reconcile, None, 50),
            }),
        'total_down_payment_company_currency': fields.function(_compute_bi_payment, method=True, multi='bipay', type='float', digits=(16, int(config['price_accuracy'])), string='Total down payment in company currency', store={
            'account.move.line': (_bi_get_invoice_from_line, None, 50),
            'account.move.reconcile': (_bi_get_invoice_from_reconcile, None, 50),
            }),
    }

account_invoice()
