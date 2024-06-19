from odoo.addons.hr_candidate.models.hr_candidate import HrStudyArea
from odoo.addons.dlink_api_utils import DlinkSerializer


class HrStudyAreaSerializer(DlinkSerializer):
    class Meta:
        model = HrStudyArea
        fields = ['id', 'name', 'score']
