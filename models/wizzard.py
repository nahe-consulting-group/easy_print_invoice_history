from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class InvoiceHistoryWizard(models.TransientModel):
    _name = "invoice.history.wizard"
    _description = "Wizard para filtrar historial de facturas"

    date_from = fields.Date("Fecha Desde")
    date_to = fields.Date("Fecha Hasta")

    def button_generate_report(self):
        active_ids = self.env.context.get("active_ids")
        _logger.info(f"Active IDs: {active_ids}")
        data = {
            "date_from": self.date_from,
            "date_to": self.date_to,
            "active_ids": self.env.context.get("active_ids", []),
        }
        return self.env.ref(
            "easy_print_invoice_history.action_report_invoice_history"
        ).report_action(self, data=data)

    def button_generate_report2(self):
        active_ids = self.env.context.get("active_ids")
        _logger.info(f"Active IDs: {active_ids}")
        data = {
            "date_from": self.date_from,
            "date_to": self.date_to,
            "active_ids": self.env.context.get("active_ids", []),
        }
        return self.env.ref(
            "easy_print_invoice_history.action_report_invoice_history2"
        ).report_action(self, data=data)
