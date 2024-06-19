from odoo.addons.dlink_api_utils.entiroment import URL_API_BASE

base_api_auth = '{}core'.format(URL_API_BASE)

hr_applicant_endpoint = '{}/hr_applicant'.format(base_api_auth)

hr_candidate_endpoint = '{}/hr_candidate'.format(base_api_auth)
hr_company_endpoint = '{}/hr_company'.format(base_api_auth)

hr_course_endpoint = '{}/hr_course'.format(base_api_auth)
hr_institution_endpoint = '{}/hr_institution'.format(base_api_auth)
hr_job_position_endpoint = '{}/hr_job_position'.format(base_api_auth)
hr_language_endpoint = '{}/hr_language'.format(base_api_auth)
hr_skill_endpoint = '{}/hr_skill'.format(base_api_auth)
hr_study_area_endpoint = '{}/hr_study_area'.format(base_api_auth)
res_country_endpoint = '{}/res_country'.format(base_api_auth)

# Res
res_company_endpoint = '{}/res_company'.format(base_api_auth)
res_department_endpoint = '{}/<int:company_id>/departments'.format(res_company_endpoint)
res_jobs_endpoint = '{}/<int:company_id>/jobs'.format(res_company_endpoint)
res_employees_endpoint = '{}/<int:company_id>/employees'.format(res_company_endpoint)
res_applicants_endpoint = '{}/<int:company_id>/applicants'.format(res_company_endpoint)

res_activities_endpoint = '{}/<int:company_id>/activities'.format(res_company_endpoint)
res_contract_type_endpoint = '{}/hr_contract_type'.format(base_api_auth)
