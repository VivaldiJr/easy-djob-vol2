from odoo import api, fields, models, _


class HrApplicant(models.Model):
    _inherit = "hr.applicant"

    candidate_id = fields.Many2one('hr.candidate', string="Candidate", help="Candidate related to this applicant")

    @api.onchange('candidate_id')
    def _onchange_candidate_id(self):
        if self.candidate_id:
            # Actualizar atributos del solicitante con los valores del candidato
            candidate = self.candidate_id

            # Actualizar campos del solicitante con los valores del candidato
            self.name = candidate.name + " " + candidate.last_name
            self.email_from = candidate.email
            self.partner_name = candidate.name + " " + candidate.last_name
            self.partner_mobile = candidate.phone
            self.partner_phone = candidate.phone

            # Aquí continúa con los demás campos que quieras sincronizar

            # Puedes agregar más lógica para sincronizar otros campos específicos que necesites


class HrCandidate(models.Model):
    _name = "hr.candidate"
    _description = "Candidate"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']

    name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    email = fields.Char(string="Email", required=True, unique=True)
    country_id = fields.Many2one('res.country', string="Country of Residence", required=True)
    email_verified = fields.Boolean(string="Email Verified", default=False)
    resume_option = fields.Selection([
        ('linkedin', 'LinkedIn'),
        ('file', 'Upload Resume File'),
        ('manual', 'Fill Manually')],
        string="Resume Upload Option",
        default='linkedin',
        required=True,
    )
    resume_file = fields.Binary(string="Resume File")
    professional_title = fields.Char(string="Professional Title")
    professional_description = fields.Text(string="Professional Description")

    # Nuevos campos para la sección de identificación
    age = fields.Integer(string="Age")
    address = fields.Char(string="Address")
    postal_code = fields.Char(string="Postal Code")
    city_province = fields.Char(string="City/Province")
    phone = fields.Char(string="Phone")

    # Relación con la experiencia profesional
    experience_ids = fields.One2many('hr.candidate.experience', 'candidate_id', string="Professional Experience")

    # Relación con el modelo de empleado
    employee_id = fields.Many2one('hr.employee', string="Employee")

    # Nuevos campos para la sección de formación escolar
    school_ids = fields.One2many('hr.candidate.school', 'candidate_id', string="Education")

    # Nuevos campos para la sección de cursos complementarios
    course_ids = fields.One2many('hr.candidate.course', 'candidate_id', string="Additional Courses")

    # Nuevos campos para la sección de idiomas
    language_ids = fields.One2many('hr.candidate.language', 'candidate_id', string="Languages")

    # Nuevos campos para la sección de habilidades
    skill_ids = fields.Many2many('hr.skill', string="Skills", help="Skills possessed by the candidate")

    # Nuevos campos para rankings y comparaciones
    overall_score = fields.Float(string="Overall Score", compute="_compute_overall_score", store=True)
    experience_score = fields.Float(string="Experience Score", compute="_compute_experience_score", store=True)
    education_score = fields.Float(string="Education Score", compute="_compute_education_score", store=True)
    skills_score = fields.Float(string="Skills Score", compute="_compute_skills_score", store=True)
    language_score = fields.Float(string="Language Score", compute="_compute_language_score", store=True)

    # Nuevos campos para el cálculo de áreas de estudio, experiencia y habilidades destacadas
    area_of_study = fields.Many2one('hr.study_area', string="Area of Study", compute="_compute_area_of_study",
                                    store=True)
    experience_count = fields.Integer(string="Experience Count", compute="_compute_experience_count", store=True)
    best_language = fields.Many2one('hr.language', string="Best Language", compute="_compute_best_language", store=True)
    best_skill = fields.Many2one('hr.skill', string="Best Skill", compute="_compute_best_skill", store=True)

    # Nuevo campo para el nivel educacional mayor
    highest_education_level = fields.Selection([
        ('no_degree', 'No Degree'),
        ('diploma', 'Diploma/Certificate'),
        ('bachelor', 'Bachelor Degree'),
        ('master', 'Master Degree'),
        ('doctorate', 'Doctorate')],
        string="Highest Education Level",
        compute="_compute_highest_education_level",
        store=True,
        readonly=True,
    )

    def score_to_stars(self):
        full_stars = int(self.overall_score)
        half_star = self.overall_score - full_stars >= 0.5
        empty_stars = 5 - full_stars - half_star
        return '★' * full_stars + ('½' if half_star else '') + '☆' * empty_stars

    @api.depends('school_ids', 'school_ids.level_attained')
    def _compute_highest_education_level(self):
        for candidate in self:
            highest_level = 'no_degree'
            education_score_map = {
                'no_degree': 0,
                'diploma': 1,
                'bachelor': 2,
                'master': 3,
                'doctorate': 4,
            }
            for school in candidate.school_ids:
                level_attained_score = education_score_map.get(school.level_attained, 0)
                if level_attained_score > education_score_map[highest_level]:
                    highest_level = school.level_attained
            candidate.highest_education_level = highest_level

    # Métodos para calcular los puntajes
    @api.depends('experience_ids', 'school_ids', 'skill_ids', 'language_ids', 'area_of_study')
    def _compute_overall_score(self):
        for candidate in self:
            candidate.overall_score = (
                                              candidate.experience_score + candidate.education_score +
                                              candidate.skills_score + candidate.language_score +
                                              candidate.area_of_study.score
                                      ) / 5.0

    @api.depends('experience_ids', 'experience_ids.achievements')
    def _compute_experience_score(self):
        for candidate in self:
            total_achievements = sum(
                len(exp.achievements) if exp.achievements else 0 for exp in candidate.experience_ids)
            candidate.experience_score = total_achievements

    @api.depends('school_ids', 'school_ids.level_attained')
    def _compute_education_score(self):
        for candidate in self:
            education_score_map = {
                'no_degree': 0,
                'diploma': 1,
                'bachelor': 2,
                'master': 3,
                'doctorate': 4,
            }
            total_education_score = sum(
                education_score_map.get(school.level_attained, 0) for school in candidate.school_ids)
            candidate.education_score = total_education_score

    @api.depends('skill_ids')
    def _compute_skills_score(self):
        for candidate in self:
            candidate.skills_score = len(candidate.skill_ids)

    @api.depends('language_ids', 'language_ids.level')
    def _compute_language_score(self):
        for candidate in self:
            language_score_map = {
                'basic': 1,
                'intermediate': 2,
                'advanced': 3,
            }
            total_language_score = sum(language_score_map.get(lang.level, 0) for lang in candidate.language_ids)
            candidate.language_score = total_language_score

    @api.depends('school_ids', 'school_ids.study_area')
    def _compute_area_of_study(self):
        for candidate in self:
            study_area_scores = {}
            for school in candidate.school_ids:
                study_area = school.study_area
                if study_area and (not study_area_scores.get(study_area) or
                                   study_area_scores[study_area] < school.level_attained_score):
                    study_area_scores[study_area] = school.level_attained_score
            best_study_area = max(study_area_scores, key=study_area_scores.get) if study_area_scores else False
            candidate.area_of_study = best_study_area

    @api.depends('experience_ids')
    def _compute_experience_count(self):
        for candidate in self:
            candidate.experience_count = len(candidate.experience_ids)

    @api.depends('language_ids', 'language_ids.level')
    def _compute_best_language(self):
        for candidate in self:
            best_language_score = 0
            best_language = False
            for lang in candidate.language_ids:
                if lang.level_score > best_language_score:
                    best_language_score = lang.level_score
                    best_language = lang.language
            candidate.best_language = best_language

    @api.depends('skill_ids', 'skill_ids.skill_score')
    def _compute_best_skill(self):
        for candidate in self:
            best_skill_score = 0
            best_skill = False
            for skill in candidate.skill_ids:
                if skill.skill_score > best_skill_score:
                    best_skill_score = skill.skill_score
                    best_skill = skill
            candidate.best_skill = best_skill


class HrCandidateExperience(models.Model):
    _name = "hr.candidate.experience"
    _description = "Candidate Experience"

    candidate_id = fields.Many2one('hr.candidate', string="Candidate", ondelete='cascade')
    company = fields.Many2one('hr.company', string="Company")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    job_positions = fields.Many2one('hr.job_position', string="Job Positions")
    achievements = fields.Text(string="Achievements")


class HrCompany(models.Model):
    _name = "hr.company"
    _description = "Companies"

    name = fields.Char(string="Company", required=True)


class HrJobPosition(models.Model):
    _name = "hr.job_position"
    _description = "Job Positions"

    name = fields.Char(string="Job Position", required=True)


class HrCandidateSchool(models.Model):
    _name = "hr.candidate.school"
    _description = "Candidate Education"

    candidate_id = fields.Many2one('hr.candidate', string="Candidate", ondelete='cascade')
    institution = fields.Many2one('hr.institution', string="Institution")
    study_area = fields.Many2one('hr.study_area', string="Study Area")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    description = fields.Text(string="Description")
    level_attained = fields.Selection([
        ('no_degree', 'No Degree'),
        ('diploma', 'Diploma/Certificate'),
        ('bachelor', 'Bachelor Degree'),
        ('master', 'Master Degree'),
        ('doctorate', 'Doctorate')],
        string="Level Attained",
        default='no_degree',
        required=True,
    )

    level_attained_score = fields.Integer(compute="_compute_level_attained_score", store=True)

    @api.depends('level_attained')
    def _compute_level_attained_score(self):
        for school in self:
            education_score_map = {
                'no_degree': 0,
                'diploma': 1,
                'bachelor': 2,
                'master': 3,
                'doctorate': 4,
            }
            school.level_attained_score = education_score_map.get(school.level_attained, 0)


class HrInstitution(models.Model):
    _name = "hr.institution"
    _description = "Institutions"

    name = fields.Char(string="Institution", required=True)


class HrStudyArea(models.Model):
    _name = "hr.study_area"
    _description = "Study Areas"

    name = fields.Char(string="Study Area", required=True)
    score = fields.Integer(string="Area Score", required=True)


class HrCandidateCourse(models.Model):
    _name = "hr.candidate.course"
    _description = "Candidate Additional Course"

    candidate_id = fields.Many2one('hr.candidate', string="Candidate", ondelete='cascade')
    course_name = fields.Many2one('hr.course', string="Course Name")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    description = fields.Text(string="Description")


class HrCourse(models.Model):
    _name = "hr.course"
    _description = "Courses"

    name = fields.Char(string="Course Name", required=True)


class HrCandidateLanguage(models.Model):
    _name = "hr.candidate.language"
    _description = "Candidate Language"

    candidate_id = fields.Many2one('hr.candidate', string="Candidate", ondelete='cascade')
    language = fields.Many2one('hr.language', string="Language")
    level = fields.Selection([
        ('basic', 'Basic'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')],
        string="Language Level",
        default='basic',
        required=True,
    )

    level_score = fields.Integer(compute="_compute_level_score", store=True)

    @api.depends('level')
    def _compute_level_score(self):
        for lang in self:
            language_score_map = {
                'basic': 1,
                'intermediate': 2,
                'advanced': 3,
            }
            lang.level_score = language_score_map.get(lang.level, 0)


class HrLanguage(models.Model):
    _name = "hr.language"
    _description = "Languages"

    name = fields.Char(string="Language", required=True)


class HrSkill(models.Model):
    _name = "hr.skill"
    _description = "Skills"

    name = fields.Char(string="Skill", required=True)

    skill_score = fields.Integer(string="Skill Score", required=True)
