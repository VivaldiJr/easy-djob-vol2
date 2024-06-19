from odoo import http
from ..serializers.res_country import ResCountrySerializer
from ..urls import res_country_endpoint
from odoo.addons.dlink_api_utils import *
from odoo.http import request


class ResCountryController(http.Controller):
    @api_key_required()
    @http.route(res_country_endpoint, methods=["GET"], type="json", auth="none", csrf=False, cors='*')
    def get(self, *args, **kwargs):
        args = request.httprequest.args
        TABLE = request.env['res.country']
        query = [("name", "ilike", args.get("q", None))]
        code = args.get("code", None)
        if code:
            query = ["&", *query, ("code", "=", code)]

        code_selecteds = args.get("code_selecteds", None)
        if code_selecteds:
            query = ["&", *query, ("code", "in", str(code_selecteds).split(','))]

        return DlinkHelper.JsonValidResponse(data=ResCountrySerializer(data=TABLE.sudo().search(query), many=True, context={"request": request}).serializer())
