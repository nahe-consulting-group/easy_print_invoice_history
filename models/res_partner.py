from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    def button_print_invoice_history(self):
        return self.env.ref(
            "easy_print_invoice_history.action_report_invoice_history"
        ).report_action(self)
