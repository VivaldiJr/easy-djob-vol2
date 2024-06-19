from odoo.addons.hr.models.hr_contract_type import ContractType
from odoo.addons.dlink_api_hr_candidate.serializers.hr_departament import HrDepartamentSerializer
from odoo.addons.dlink_api_hr_candidate.serializers.res_company import ResCompanySerializer
from odoo.addons.hr.models.hr_job import Job
from odoo.addons.hr_candidate.models.hr_candidate import HrJobPosition
from odoo.addons.dlink_api_utils import DlinkSerializer


class HrContractTypeSerializer(DlinkSerializer):
    class Meta:
        model = ContractType
        fields = ['id', 'name']


class HrJobSerializer(DlinkSerializer):
    company_id = ResCompanySerializer()
    department_id = HrDepartamentSerializer()
    contract_type_id = HrContractTypeSerializer()

    class Meta:
        model = Job
        fields = ['id', 'name',
                  'contract_type_id',
                  'expected_employees',
                  'no_of_employee',
                  'no_of_recruitment',
                  'no_of_hired_employee',
                  'application_ids',
                  'application_count',
                  'all_application_count',
                  'new_application_count',
                  'old_application_count',
                  'applicant_hired',
                  'description',
                  'requirements',
                  'department_id',
                  'company_id',
                  'address_id',
                  'work_process',
                  'address',
                  'contract_detail',
                  'min_salary',
                  'max_salary',
                  'currency_id',
                  'select_frequency',
                  ]

class HrJobPositionSerializer(DlinkSerializer):
    class Meta:
        model = HrJobPosition
        fields = ['id', 'name']
