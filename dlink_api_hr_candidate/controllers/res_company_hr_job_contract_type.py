from odoo import http
from ..serializers.hr_job_contract_type import HrJobContractTypeSerializer

from ..urls import res_contract_type_endpoint
from odoo.addons.dlink_api_utils import *
from odoo.http import request
from odoo.addons.dlink_api_auth.controller.decorators import token_required


class HrJobContractTypeController(http.Controller):
    @token_required
    @api_key_required()
    @http.route(res_contract_type_endpoint, methods=["GET"], type="json", auth="none", csrf=False, cors='*')
    def get(self, *args, company=None, **kwargs):
        TABLE = request.env['hr.contract.type']
        return DlinkHelper.JsonValidResponse(data=HrJobContractTypeSerializer(data=TABLE.sudo().search([]), many=True).serializer())
