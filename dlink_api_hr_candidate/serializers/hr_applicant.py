from odoo.addons.dlink_api_auth.serializers.user import UserSerializer
from odoo.addons.hr_recruitment.models.hr_recruitment import RecruitmentDegree
from odoo.addons.hr_recruitment.models.hr_recruitment import ApplicantCategory
from odoo.addons.hr_candidate.models.hr_candidate import HrApplicant
from odoo.addons.dlink_api_utils import DlinkSerializer


class ApplicantCategorySerializer(DlinkSerializer):
    class Meta:
        model = ApplicantCategory
        fields = ['id', 'name', 'color']


class RecruitmentDegreeSerializer(DlinkSerializer):
    class Meta:
        model = RecruitmentDegree
        fields = ['id', 'name', 'sequence']


class HrApplicantSerializer(DlinkSerializer):
    # candidate_id = HrCandidateSerializer()
    user_id = UserSerializer()
    categ_ids = ApplicantCategorySerializer(many=True)
    type_id = RecruitmentDegreeSerializer()

    class Meta:
        model = HrApplicant
        fields = ['id', 'name', 'description', 'user_id', 'type_id', 'priority', 'create_date', 'availability', 'date_open',
                  'date_closed',
                  'categ_ids', 'candidate_id', 'job_id']
