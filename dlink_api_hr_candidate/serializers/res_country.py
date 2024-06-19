from odoo.addons.dlink_api_utils.utils.domain import domain
from odoo.addons.dlink_api_utils import DlinkSerializer
from odoo.addons.base.models.res_country import Country


class ResCountrySerializer(DlinkSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'code', 'phone_code', ]
        functions = ['image']

    def image(self, obj):
        request = self.context.get('request', None)
        return "{}{}".format(domain(request), obj.image_url) if obj.image_url else None
