# Copyright (C) 2022 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.tools import is_html_empty


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange("partner_id", "company_id")
    def onchange_partner_id(self):
        if not is_html_empty(self.partner_id.sale_note):
            self.note = self.partner_id.sale_note
        elif (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("sale.use_sale_note")
        ):
            self.note = self.company_id.sale_note
