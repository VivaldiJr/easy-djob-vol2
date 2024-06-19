from odoo.addons.dlink_api_hr_candidate.serializers.hr_language import HrLanguageSerializer
from odoo.addons.hr_candidate.models.hr_candidate import HrCandidateLanguage
from odoo.addons.dlink_api_utils import DlinkSerializer


class HrCandidateLanguageSerializer(DlinkSerializer):
    language = HrLanguageSerializer()

    class Meta:
        model = HrCandidateLanguage
        fields = ['id', 'candidate_id', 'language', 'level', 'level_score']
