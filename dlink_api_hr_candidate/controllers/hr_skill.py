from odoo import http
from ..serializers.hr_skill import HrSkillSerializer
from ..urls import hr_skill_endpoint
from odoo.addons.dlink_api_utils import *
from odoo.http import request


class HrSkillController(http.Controller):
    @api_key_required()
    @http.route(hr_skill_endpoint, methods=["GET"], type="json", auth="none", csrf=False, cors='*')
    def get(self, *args, **kwargs):
        args = request.httprequest.args
        TABLE = request.env['hr.skill']
        return DlinkHelper.JsonValidResponse(
            data=HrSkillSerializer(data=TABLE.sudo().search([("name", "ilike", args.get("q", ""))]), many=True).serializer())

    @api_key_required()
    @fields_required_json(fields=[
        FieldRequired(key="name", type='str')
    ])
    @http.route(hr_skill_endpoint, methods=["POST"], type="json", auth="none", csrf=False, cors='*')
    def post(self, *args, **kwargs):
        print(kwargs)
        kwargs['skill_score'] = 0
        TABLE = request.env['hr.skill']
        return DlinkHelper.JsonValidResponse(data=HrSkillSerializer(data=TABLE.sudo().create(kwargs)).serializer())
