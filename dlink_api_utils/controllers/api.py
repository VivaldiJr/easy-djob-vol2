from werkzeug.routing import Rule

from odoo.http import request
from .. import DlinkHelper, api_key_required
from ..entiroment import URL_API_BASE
from odoo import http


class URLS(http.Controller):
    @api_key_required()
    @http.route("/api/urls/", methods=["GET"], type="json", auth="none", csrf=False, cors='*')
    def get(self, *args, **kwargs):

        routing = http.root.get_db_router('odoo')

        api_key_required = request.env['ir.config_parameter'].sudo().get_param('dlink_api_utils.api_key_required')
        api = request.env['ir.config_parameter'].sudo().get_param('dlink_api_utils.api')

        urls = []
        for rule in routing.iter_rules():
            url: Rule = rule.rule

            if str(url).__contains__(URL_API_BASE):
                urls.append(rule.endpoint.routing)
        return DlinkHelper.JsonValidResponse(data=urls)
