from odoo.addons.hr_candidate.models.hr_candidate import HrInstitution
from odoo.addons.dlink_api_utils import DlinkSerializer


class HrInstitutionSerializer(DlinkSerializer):
    class Meta:
        model = HrInstitution
        fields = ['id', 'name']
