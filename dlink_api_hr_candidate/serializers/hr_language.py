from odoo.addons.hr_candidate.models.hr_candidate import HrLanguage
from odoo.addons.dlink_api_utils import DlinkSerializer


class HrLanguageSerializer(DlinkSerializer):
    class Meta:
        model = HrLanguage
        fields = ['id', 'name']
