from odoo.addons.dlink_api_ntizu_job_conn.urls import res_currency_endpoint
from odoo.addons.dlink_api_ntizu_job_conn.serializers.res_currency import ResCurrencySerializer
from odoo import http
from odoo.addons.dlink_api_utils import api_key_required, DlinkHelper
from odoo.http import request


class ResCurrencyController(http.Controller):
    @api_key_required()
    @http.route(res_currency_endpoint, methods=["GET"], type="json", auth="none", csrf=False, cors='*')
    def currency(self, *args, **kwargs):
        args = request.httprequest.args
        TABLE_CURRENCY = request.env['res.currency']
        query_search = [("active", '=', True)]
        q = args.get('q', None)
        if q:
            query_search.append(('name', 'ilike', q))
        currencies = TABLE_CURRENCY.sudo().search(query_search)

        return DlinkHelper.JsonValidResponse(ResCurrencySerializer(currencies, context={"request": request}, many=True).serializer())
