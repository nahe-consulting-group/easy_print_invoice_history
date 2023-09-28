from odoo import api, models
from datetime import datetime

import logging

_logger = logging.getLogger(__name__)


class CustomerInvoiceHistory(models.AbstractModel):
    _name = "report.easy_print_invoice_history.report_invoice_history"

    @api.model
    def _get_report_values(self, docids, data=None):
        invoices = self.env["account.move"].search(
            [
                ("partner_id", "in", docids),
                ("move_type", "in", ["out_invoice", "out_refund"]),
                ("state", "not in", ["draft", "canceled"]),
            ]
        )

        partner = self.env["res.partner"].search(
            [
                ("id", "=", docids[0]),
            ],
            limit=1,
        )

        payments = self.env["account.payment.group"].search(
            [("partner_id", "in", docids)]
        )

        sorted_data = []

        for inv in invoices:
            payment_groups = ", ".join(
                [pg.display_name for pg in inv.payment_group_ids]
            )

            credit = 0.0
            debit = 0.0
            if inv.move_type == "out_refund":
                credit = round(inv.amount_total, 2)
            elif inv.move_type == "out_invoice":
                debit = round(inv.amount_total, 2)

            sorted_data.append(
                {
                    "date": inv.invoice_date,
                    "name": inv.name,
                    "credit": credit,
                    "debit": debit,
                    "payment_groups": payment_groups,
                }
            )

        for pay in payments:
            sorted_data.append(
                {
                    "date": pay.payment_date,
                    "name": pay.name,
                    "credit": round(pay.payments_amount, 2),
                    "debit": 0.0,
                    "payment_groups": "",
                }
            )

        # Convertir datetime.datetime a datetime.date
        for entry in sorted_data:
            if isinstance(entry["date"], datetime):
                entry["date"] = entry["date"].date()

        # Filtrar entradas que no tienen fecha
        sorted_data = [entry for entry in sorted_data if entry["date"]]

        # Ordenar las entradas
        try:
            sorted_data = sorted(sorted_data, key=lambda x: x["date"])
        except Exception as e:
            _logger.error(f"Error al ordenar los datos: {e}")

        return {
            "docs": self.env["res.partner"].browse(docids),
            "sorted_data": sorted_data,
        }
