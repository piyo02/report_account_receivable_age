from odoo import api, fields, models
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

import logging
_logger = logging.getLogger(__name__)

class ReportAccountReceivableAge(models.TransientModel):
    _name = "report.account.receivable.age"

    age = fields.Integer(string='Umur Piutang', required=True)
    customers = fields.Many2many('res.partner', string='Pelanggan', required=False)

    @api.multi
    def print_report_account_receivable_age(self):
        groupby_dict = {}

        if len(self.customers) == 0:
            self.customers = self.env['res.partner'].search([
                ('customer', '=', True)
            ],
            order='name asc')

        today = date.today()
        date_invoice = ( today + timedelta( days=(self.age*-1) ) ).strftime("%Y-%m-%d")
        customer_detail = []
        for customer in self.customers:
            invoices = self.env['account.invoice'].search([
                ('date_invoice', '=', date_invoice),
                ('partner_id', '=', customer.id)
            ])
            customer_temp = []
            customer_invoices = []
            customer_temp.append(customer.credit_limit)
            for invoice in invoices:
                customer_invoice = []
                customer_invoice.append(invoice.number)         #0
                customer_invoice.append(invoice.payment_term_id.name)#1
                customer_invoice.append(invoice.date_invoice)   #2
                customer_invoice.append(invoice.user_id.name)   #3
                customer_invoice.append(invoice.date_due)       #4
                customer_invoice.append(invoice.amount_total)   #5
                customer_invoice.append(invoice.residual)       #6
                customer_invoices.append(customer_invoice)      
            
            customer_temp.append(customer_invoices)

            if len(customer_invoices) > 0:
                customer_detail.append(customer_temp)
        
        if len(customer_detail) > 0:
            groupby_dict[customer.display_name] = customer_detail
        
        datas = {
            'ids': self.ids,
            'model': 'report.account.receivable.age',
            'form': groupby_dict,
            'age': self.age,
        }
        return self.env['report'].get_action(self,'report_account_receivable_age.report_temp', data=datas)

    
    def _prepare_report_account_receivable(self):
        self.ensure_one()
        return {
            'ids': self.ids,
            'model': 'report.account.receivable.age',
            'data': groupby_dict,
            'age': self.age,
        }

    def _export(self, report_type):
        """Default export is PDF."""
        model = self.env['report_trial_balance_qweb']
        report = model.create(self._prepare_report_account_receivable())
        return report.print_report(report_type)