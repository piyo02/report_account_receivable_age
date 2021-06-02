from odoo import api, models


class ReportAccountReceivableAgeTemp(models.AbstractModel):
    _name = 'report.report_account_receivable_age.report_temp'

    @api.model
    def render_html(self, docids, data=None):
        docargs =  {
            'doc_ids': data.get('ids'),
            'doc_model': data.get('model'),
            'data': data['form'],
            'age': data['age'],
        }
        print "===================docargs",docargs
        return self.env['report'].render('report_account_receivable_age.report_temp', docargs)
