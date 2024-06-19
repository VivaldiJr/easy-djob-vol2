from odoo.addons.dlink_api_hr_candidate.serializers.res_country import ResCountrySerializer
from odoo.addons.dlink_api_hr_candidate.serializers.hr_candidate_course import HrCandidateCourseSerializer
from odoo.addons.dlink_api_hr_candidate.serializers.hr_candidate_language import HrCandidateLanguageSerializer
from odoo.addons.dlink_api_hr_candidate.serializers.hr_candidate_school import HrCandidateSchoolSerializer
from odoo.addons.dlink_api_hr_candidate.serializers.hr_language import HrLanguageSerializer
from odoo.addons.dlink_api_hr_candidate.serializers.hr_study_area import HrStudyAreaSerializer
from odoo.addons.dlink_api_hr_candidate.serializers.hr_skill import HrSkillSerializer
from odoo.addons.dlink_api_hr_candidate.serializers.hr_candidate_experience import HrCandidateExperienceSerializer

from odoo.addons.dlink_api_utils.utils.domain import domain
from odoo.addons.hr_candidate.models.hr_candidate import HrCandidate
from odoo.addons.dlink_api_utils import DlinkSerializer

_fields = [
    'id',
    'name',
    'last_name',
    'email',
    'country_id',

    'email_verified',
    'resume_option',

    'professional_title',
    'professional_description',
    # Nuevos campos para la sección de identificación
    'age',
    'address',
    'postal_code',
    'city_province',
    'phone',
    # Relaciones
    'experience_ids',
    'employee_id',
    'school_ids',
    'course_ids',
    'language_ids',
    'skill_ids',
    # Nuevos campos para rankings y comparaciones
    'overall_score',
    'experience_score',
    'education_score',
    'skills_score',
    'language_score',
    # Nuevos campos para el cálculo de áreas de estudio, experiencia y habilidades destacadas
    'area_of_study',
    'experience_count',
    'best_language',
    'best_skill',
    'highest_education_level'
]


class HrCandidateSerializer(DlinkSerializer):
    country_id = ResCountrySerializer()
    experience_ids = HrCandidateExperienceSerializer(many=True)
    school_ids = HrCandidateSchoolSerializer(many=True)
    course_ids = HrCandidateCourseSerializer(many=True)
    language_ids = HrCandidateLanguageSerializer(many=True)
    skill_ids = HrSkillSerializer(many=True)

    area_of_study = HrStudyAreaSerializer(many=True)
    best_language = HrLanguageSerializer()

    class Meta:
        model = HrCandidate
        fields = _fields
        nif = ['email_verified']
        functions = ['avatar_256', 'resume_field']

    def avatar_256(self, obj):
        request = self.context.get('request', None)

        return '%s/files/%s/%s/%s' % (domain(request), obj._name, obj.id, "avatar_256") if obj.avatar_256 and request else None

    def resume_field(self, obj):
        request = self.context.get('request', None)

        return '%s/files/%s/%s/%s' % (domain(request), obj._name, obj.id, "resume_file") if obj.resume_file else None
