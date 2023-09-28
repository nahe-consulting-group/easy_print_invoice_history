{
    "name": "Easy Print Invoice History",
    "summary": """
        Allows to print invice and payments history for any partner with only 1 button in partner form. 
    """,
    "author": "Nahe Consulting Group",
    "website": "https://www.nahe.com.ar",
    "license": "AGPL-3",
    "category": "Accounting",
    "version": "15.0.1.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "depends": [
        "base",
        "contacts",
        "account",
    ],
    "data": [
        "views/res_partner_view.xml",
        "views/report_action.xml",
        "views/template_invoice_history.xml",
    ],
}
