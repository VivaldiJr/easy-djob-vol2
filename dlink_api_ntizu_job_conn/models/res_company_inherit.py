from odoo import models


class ResCompanyInherit(models.Model):
    _inherit = 'res.company'  # Indica que estás heredando el modelo 'res.company'

    # def iap_enrich_auto(self):
    #     """ Enrich company. This method should be called by automatic processes
    #     and a protection is added to avoid doing enrich in a loop. """
    #     if self.env.user and self.env.user._is_system():
    #         for company in self.filtered(lambda company: not company.iap_enrich_auto_done):
    #             company._enrich()
    #         self.iap_enrich_auto_done = True
    #     return True
