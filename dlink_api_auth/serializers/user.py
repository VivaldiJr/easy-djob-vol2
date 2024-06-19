from odoo.addons.dlink_api_utils.utils.domain import domain
from ..serializers.partner import PartnerSerializer
from odoo.addons.dlink_api_utils import DlinkSerializer
from odoo.addons.hr.models.res_users import User


class UserSerializer(DlinkSerializer):
    partner_id = PartnerSerializer()

    class Meta:
        model = User
        fields = ["id", "email", "login", "name", "partner_id", "type", "company_type", "company_id", "lang", "tz"]
        functions = ["avatar", "manager", "ntizu"]

    def avatar(self, obj):
        request = self.context.get('request', None)

        return '%s/files/%s/%s/%s' % (domain(request), obj._name, obj.id, "image_256") if obj.image_256 else None

    def manager(self, user):
        return user.has_group('base.group_erp_manager')

    def ntizu(self, user):
        try:
            request = self.context.get('request', None)
            table = request.env['representative.ntizu.company.request']
            companies = table.sudo().search([("email", "=", user.email)]).mapped('company_id')
            return companies.id if companies else None
        except:
            return None
