from odoo.addons.hr_candidate.models.hr_candidate import HrSkill
from odoo.addons.dlink_api_utils import DlinkSerializer


class HrSkillSerializer(DlinkSerializer):
    class Meta:
        model = HrSkill
        fields = ['id', 'name', 'skill_score']
