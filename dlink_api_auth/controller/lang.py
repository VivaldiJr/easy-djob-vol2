from odoo import http
from ..serializers.lang import LanguageSerializer

from ..urls import language_endpoint

from odoo.addons.dlink_api_utils import *
from odoo.http import request


class JsonDLinkLanguage(http.Controller):
    @api_key_required()
    @http.route(language_endpoint, methods=["GET"], type="json", auth="none", csrf=False, cors='*')
    def get(self, *args, **kwargs):
        TABLE_LANGUAGE = request.env['res.lang']
        return DlinkHelper.JsonValidResponse(data=LanguageSerializer(TABLE_LANGUAGE.sudo().search([]), many=True, context={"request": request}).serializer())
