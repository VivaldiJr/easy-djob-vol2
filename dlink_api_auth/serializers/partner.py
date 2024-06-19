from odoo.addons.base.models.res_partner import Partner
from odoo.addons.dlink_api_utils import DlinkSerializer
from odoo.addons.dlink_api_utils.utils.domain import domain


class PartnerSerializer(DlinkSerializer):
    class Meta:
        model = Partner
        fields = ["id", "name", "is_company", "active", "company_id"]
        nif = ['active', 'is_company']
        functions = ['avatar']

    def avatar(self, obj):
        request = self.context.get('request', None)

        return '%s/files/%s/%s/%s' % (domain(request), obj._name, obj.id, "image_256") if obj.image_256 else None
