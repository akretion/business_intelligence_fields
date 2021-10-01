# Copyright 2011-2021 Akretion France (http://www.akretion.com/)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.depends(
        'move_id.currency_id', 'move_id.state',
        'move_id.date', 'move_id.company_id', 'price_unit')
    def _compute_amount_in_company_currency(self):
        for line in self:
            price_unit_cc = 0.0
            move = line.move_id
            if not line.display_type and line.price_unit and move:
                date = move.date or fields.Date.context_today(self)
                price_unit_cc = move.currency_id._convert(
                    line.price_unit, move.company_id.currency_id,
                    move.company_id, date)
            line.price_unit_company_currency = price_unit_cc

    price_unit_company_currency = fields.Float(
        compute='_compute_amount_in_company_currency',
        digits='Product Price',
        string='Unit Price in Company Currency', store=True)


class AccountMove(models.Model):
    _inherit = "account.move"

    company_currency_id = fields.Many2one(store=True)
