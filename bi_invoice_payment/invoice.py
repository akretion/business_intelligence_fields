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
from datetime import datetime, timedelta
from tools import config
import decimal_precision as dp

class account_invoice(osv.osv):
    _inherit = "account.invoice"

    def _compute_bi_payment(self, cr, uid, ids, name, arg, context=None):
        result = {}
        for inv in self.browse(cr, uid, ids, context=context):

            # To test the down payment algo, you have to consider at least these scenarios :
            # Scenario 1 :
            # 16/05 : payment of 9000 €
            # 17/05 : invoice 1 of 8000 €  => DP of I1 = 8000 €
            # 18/05 : invoice 2 of 2000 €  => DP of I1 = 8000 €, DP of I2 = 1000 €
            # 19/05 : final payment of 1000 € => no change in DP

            # Scenario 2
            # 16/05 : invoice 1 of 3000 €
            # 17/05 : invoice 2 of 2000 €
            # 18/05 : payment of 5000 € => all down payment must stay at 0
            # (the risk is that DP of invoice 2 becomes negative)

            # Scenario 3 :
            # 16/05 : refund of -1000 € (to cancel an invoice that was already paid)
            # 17/05 : invoice 1 of 3000 € => DP of I1 = 0
            # 18/05 : payment of 2000 €

            date_final_payment_to_write = False
            max_date_all_journals = False
            max_date_cash_journal = False
            payment_delay_days_to_write = False
            overdue_delay_days_to_write = False
            total_down_pay_to_write = 0.0
            total_down_pay = 0.0
            # no final payment date nor down payment for refunds
            if inv.type in ('in_invoice', 'out_invoice'):
                for payment in inv.payment_ids:
                    if inv.reconciled:
                        if payment.date and payment.date > max_date_all_journals:
                            max_date_all_journals = payment.date
                        if payment.date and payment.journal_id and payment.journal_id.type == 'cash' and payment.date > max_date_cash_journal:
                            max_date_cash_journal = payment.date

                    if payment.date <= inv.date_invoice:
                        if payment.journal_id and payment.journal_id.type == 'cash':
                            total_down_pay += payment.credit
                        elif payment.journal_id and payment.journal_id.type == 'sale':
                            total_down_pay -= payment.debit

                # We have a final payment date only when the invoice if reconciled
                # We also need to check if there are some payment lines
                # because, when we unreconcile a payment voucher, the payment lines
                # are unlinked but reconcile is still True for a little amount of time
                if inv.reconciled and inv.payment_ids:
                    # If we have at least one pay line in cash journal, we take the max
                    # date of the payment lines in cash journal
                    if max_date_cash_journal:
                        date_final_payment_to_write = max_date_cash_journal
                    # Otherwise, we take the max date of all the payment lines
                    elif max_date_all_journals:
                        date_final_payment_to_write = max_date_all_journals

                    # Computing payment delays
                    final_date_datetime = datetime.strptime(date_final_payment_to_write, '%Y-%m-%d')
                    if not inv.date_due or date_final_payment_to_write <= inv.date_due:
                        overdue_delay_days_to_write = 0
                    else:
                        due_date_datetime = datetime.strptime(inv.date_due, '%Y-%m-%d')
                        overdue_delay_days_to_write = (final_date_datetime - due_date_datetime).days

                    if date_final_payment_to_write <= inv.date_invoice:
                        payment_delay_days_to_write = 0
                    else:
                        invoice_date_datetime = datetime.strptime(inv.date_invoice, '%Y-%m-%d')
                        payment_delay_days_to_write = (final_date_datetime - invoice_date_datetime).days


                if inv.currency_id == inv.company_id.currency_id:
                    amount_total_company_currency = inv.amount_total
                else:
                    amount_total_company_currency = self.pool.get('res.currency').compute(cr, uid, inv.currency_id.id, inv.company_id.currency_id.id, inv.amount_total, context=context)
                # No negative down payment
                if total_down_pay < 0:
                    total_down_pay_to_write = 0.0
                # Limit down payment to the total amount of invoice
                elif total_down_pay > amount_total_company_currency:
                    total_down_pay_to_write = amount_total_company_currency
                else:
                    total_down_pay_to_write = total_down_pay


            result[inv.id] = {
                    'date_final_payment': date_final_payment_to_write,
                    'overdue_delay_days': overdue_delay_days_to_write,
                    'payment_delay_days': payment_delay_days_to_write,
                    'total_down_payment_company_currency': total_down_pay_to_write,
            }
        #print "result =", result
        return result

    def _bi_get_invoice_from_line(self, cr, uid, ids, context=None):
        #print "_bi_get_invoice_from_line SENDING ALL IDS"
        #return self.pool.get('account.invoice').search(cr, uid, [], context=context)
        return self.pool.get('account.invoice')._get_invoice_from_line(cr, uid, ids, context=context)

    def _bi_get_invoice_from_reconcile(self, cr, uid, ids, context=None):
        return self.pool.get('account.invoice')._get_invoice_from_reconcile(cr, uid, ids, context=context)

    _columns = {
        'date_final_payment': fields.function(_compute_bi_payment, method=True, multi='bipay', type='date', string='Final payment date', store={
            'account.move.line': (_bi_get_invoice_from_line, None, 50),
            'account.move.reconcile': (_bi_get_invoice_from_reconcile, None, 50),
            }),
        'payment_delay_days': fields.function(_compute_bi_payment, method=True, multi='bipay', type='integer', string='Payment delay in days', store={
            'account.move.line': (_bi_get_invoice_from_line, None, 50),
            'account.move.reconcile': (_bi_get_invoice_from_reconcile, None, 50),
            }),
        'overdue_delay_days': fields.function(_compute_bi_payment, method=True, multi='bipay', type='integer', string='Overdue delay in days', store={
            'account.move.line': (_bi_get_invoice_from_line, None, 50),
            'account.move.reconcile': (_bi_get_invoice_from_reconcile, None, 50),
            }),
        'total_down_payment_company_currency': fields.function(_compute_bi_payment, method=True, multi='bipay', type='float', digits_compute=dp.get_precision('Account'), string='Total down payment in company currency', store={
            'account.move.line': (_bi_get_invoice_from_line, None, 50),
            'account.move.reconcile': (_bi_get_invoice_from_reconcile, None, 50),
            }),
    }

account_invoice()
