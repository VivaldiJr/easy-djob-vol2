# -*- coding: utf-8 -*-
# from odoo import http


# class HrCandidate(http.Controller):
#     @http.route('/hr_candidate/hr_candidate', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_candidate/hr_candidate/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_candidate.listing', {
#             'root': '/hr_candidate/hr_candidate',
#             'objects': http.request.env['hr_candidate.hr_candidate'].search([]),
#         })

#     @http.route('/hr_candidate/hr_candidate/objects/<model("hr_candidate.hr_candidate"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_candidate.object', {
#             'object': obj
#         })
