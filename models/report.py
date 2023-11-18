from odoo import api, models
from datetime import datetime
from odoo.fields import Date
import logging
import locale

_logger = logging.getLogger(__name__)


class CustomerInvoiceHistory(models.AbstractModel):
    _name = "report.easy_print_invoice_history.report_invoice_history"

    @api.model
    def _get_report_values(self, docids, data=None):
        # Configurar la localización para formatear los números
        locale.setlocale(locale.LC_ALL, "es_ES.UTF-8")
        if docids is None:
            docids = data.get("active_ids", [])
        invoices = self.env["account.move"].search(
            [
                "&",
                "&",
                "&",
                ("partner_id", "in", docids),
                ("move_type", "in", ["out_invoice", "out_refund"]),
                ("state", "not in", ["draft", "canceled"]),
                "|",
                ("journal_id.l10n_latam_use_documents", "=", True),
                ("journal_id", "=", 14),
            ]
        )

        partner = self.env["res.partner"].search(
            [
                ("id", "=", docids[0]),
            ],
            limit=1,
        )

        payments = self.env["account.payment.group"].search(
            [("partner_id", "in", docids), ("receiptbook_id", "=", 1)]
        )

        sorted_data = []

        for inv in invoices:
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
                }
            )

        for pay in payments:
            sorted_data.append(
                {
                    "date": pay.payment_date,
                    "name": pay.name,
                    "credit": round(pay.payments_amount, 2),
                    "debit": 0.0,
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

        report_date = datetime.now().strftime("%Y-%m-%d")

        date_from = Date.from_string(data.get("date_from", "1900-01-01"))
        date_to = Date.from_string(data.get("date_to", "2099-12-31"))

        _logger.info(f"Date From: {date_from}, Date To: {date_to}")  # Log de las fechas

        return {
            "docs": self.env["res.partner"].browse(docids),
            "sorted_data": sorted_data,
            "report_date": report_date,
            "date_from": date_from,
            "date_to": date_to,
        }


class CustomerInvoiceHistory2(models.AbstractModel):
    _name = "report.easy_print_invoice_history.report_invoice_history2"

    @api.model
    def _get_report_values(self, docids, data=None):
        if docids is None:
            docids = data.get("active_ids", [])
        invoices = self.env["account.move"].search(
            [
                ("partner_id", "in", docids),
                ("move_type", "in", ["out_invoice", "out_refund"]),
                ("state", "not in", ["draft", "canceled"]),
                ("journal_id.l10n_latam_use_documents", "=", False),
                ("journal_id", "!=", 14),
            ]
        )

        partner = self.env["res.partner"].search(
            [
                ("id", "=", docids[0]),
            ],
            limit=1,
        )

        payments = self.env["account.payment.group"].search(
            [("partner_id", "in", docids), ("receiptbook_id", "=", 3)]
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
                }
            )

        for pay in payments:
            sorted_data.append(
                {
                    "date": pay.payment_date,
                    "name": pay.name,
                    "credit": round(pay.payments_amount, 2),
                    "debit": 0.0,
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

        report_date = datetime.now().strftime("%Y-%m-%d")

        date_from = Date.from_string(data.get("date_from", "1900-01-01"))
        date_to = Date.from_string(data.get("date_to", "2099-12-31"))

        _logger.info(f"Date From: {date_from}, Date To: {date_to}")  # Log de las fechas

        return {
            "docs": self.env["res.partner"].browse(docids),
            "sorted_data": sorted_data,
            "report_date": report_date,
            "date_from": date_from,
            "date_to": date_to,
        }
