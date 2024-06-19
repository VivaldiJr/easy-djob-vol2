from odoo.addons.dlink_api_hr_candidate.serializers.hr_institution import HrInstitutionSerializer
from odoo.addons.dlink_api_hr_candidate.serializers.hr_study_area import HrStudyAreaSerializer
from odoo.addons.hr_candidate.models.hr_candidate import HrCandidateSchool
from odoo.addons.dlink_api_utils import DlinkSerializer


class HrCandidateSchoolSerializer(DlinkSerializer):
    institution = HrInstitutionSerializer()
    study_area = HrStudyAreaSerializer()

    class Meta:
        model = HrCandidateSchool
        fields = ['id', 'candidate_id', 'study_area', 'institution', 'start_date', 'end_date', 'description', 'level_attained', 'level_attained_score']
