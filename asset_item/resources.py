from import_export import resources

from .models import Employee

class EmployeeResource(resources.ModelResource):
    class meta:
        module= Employee
        skip_unchanged = True
        report_skipped = True
        exclude = ('id',)
        import_id_fields = ('employee_id', 'name',
                            'designation', 'department', 'company',)
        #export_order = ('edx_id', 'edx_email')
