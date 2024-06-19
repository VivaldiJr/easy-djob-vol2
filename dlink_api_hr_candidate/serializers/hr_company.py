from odoo.addons.hr_candidate.models.hr_candidate import HrCompany
from odoo.addons.dlink_api_utils import DlinkSerializer


class HrCompanySerializer(DlinkSerializer):
    class Meta:
        model = HrCompany
        fields = ['id', 'name']
