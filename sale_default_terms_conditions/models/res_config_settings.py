# Copyright 2020 - TODAY, Marcel Savegnago - Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    sale_note = fields.Html(
        related="company_id.sale_note",
        string="Sale Terms & Conditions",
        readonly=False,
    )

    use_sale_note = fields.Boolean(
        string="Use Sale Default Terms & Conditions",
        config_parameter="sale.use_sale_note",
    )
