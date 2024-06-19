from odoo.addons.dlink_api_utils.utils.domain import domain
from odoo.addons.base.models.res_company import Company
from odoo.addons.dlink_api_utils import DlinkSerializer


class ResCompanySerializer(DlinkSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'street', 'zip', 'city', 'email', 'phone', 'website', ]
        functions = ['image']

    def image(self, obj):
        request = self.context.get('request', None)

        return '%s/files/%s/%s/%s' % (domain(request), obj._name, obj.id, "logo") if obj.logo else None
