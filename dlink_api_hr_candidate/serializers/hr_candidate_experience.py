from odoo.addons.dlink_api_hr_candidate.serializers.hr_job_position import HrJobPositionSerializer
from odoo.addons.dlink_api_hr_candidate.serializers.hr_company import HrCompanySerializer
from odoo.addons.hr_candidate.models.hr_candidate import HrCandidateExperience
from odoo.addons.dlink_api_utils import DlinkSerializer


class HrCandidateExperienceSerializer(DlinkSerializer):
    company = HrCompanySerializer()
    job_positions = HrJobPositionSerializer()

    class Meta:
        model = HrCandidateExperience
        fields = ['id', 'start_date', 'end_date', 'company', 'candidate_id', 'job_positions', 'achievements']
