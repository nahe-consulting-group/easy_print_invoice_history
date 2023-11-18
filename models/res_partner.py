from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    def button_print_invoice_history(self):
        return {
            "name": "Seleccionar Rango de Fechas",
            "type": "ir.actions.act_window",
            "res_model": "invoice.history.wizard",
            "view_mode": "form",
            "view_id": self.env.ref(
                "easy_print_invoice_history.view_invoice_history_wizard_form"
            ).id,
            "target": "new",
        }
        # return self.env.ref(
        #    "easy_print_invoice_history.action_report_invoice_history"
        # ).report_action(self)

    # def button_print_invoice_history2(self):
    # return self.env.ref(
    #    "easy_print_invoice_history.action_report_invoice_history2"
    # ).report_action(self)
