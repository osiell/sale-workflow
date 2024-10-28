# Copyright (C) 2022 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestSale(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.env.ref("uom.product_uom_hour")
        cls.product_order = cls.env["product.product"].create(
            {
                "name": "Zed+ Antivirus",
                "standard_price": 235.0,
                "list_price": 280.0,
                "type": "consu",
                "uom_id": uom_unit.id,
                "uom_po_id": uom_unit.id,
                "sale_method": "sale",
                "default_code": "PROD_ORDER",
                "taxes_id": False,
            }
        )
        cls.partner_a.write(
            {"sale_note": "Sale Default Terms and Conditions Partner"}
        )

    def test_onchange_partner_id(self):
        sale_order = (
            self.env["sale.order"]
            .with_context(tracking_disable=True)
            .create(
                {
                    "partner_id": self.partner_a.id,
                }
            )
        )
        sale_order.onchange_partner_id()
        SaleOrderLine = self.env["sale.order.line"].with_context(
            tracking_disable=True
        )
        SaleOrderLine.create(
            {
                "name": self.product_order.name,
                "product_id": self.product_order.id,
                "product_qty": 10.0,
                "product_uom": self.product_order.uom_id.id,
                "price_unit": self.product_order.list_price,
                "order_id": sale_order.id,
                "taxes_id": False,
            }
        )

        self.partner_a.write({"sale_note": False})

        self.env["ir.config_parameter"].set_param("sale.use_sale_note", "Test")

        sale_order.onchange_partner_id()
