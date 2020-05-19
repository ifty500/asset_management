from django import forms 
from .models import Company, Item, Employee, Department
from django .contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']



class CompanyForm(forms.ModelForm):
    
    class Meta:
        model = Company
        fields = ("name","short_name", "address","phone" ,"status")

    # Validates the Company Name Field
    def clean_name(self):
        name = self.cleaned_data.get('name')
        for instance in Company.objects.all():
            if instance.name == name:
                raise forms.ValidationError(name + ' is already exist')
        if (name == ""):
            raise forms.ValidationError('This field cannot be left blank')
        return name

class CompanySearchForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name','short_name', 'export_to_CSV']



class ItemForm(forms.ModelForm):
    
    class Meta:
        model = Item
        fields = ("item_name","description","item_type", "code", "unit","company","department", "purchase_date","employee")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].queryset= Department.objects.none()
        self.fields['employee'].queryset= Department.objects.none() 
        
        

        if 'company' in self.data:
            try:
                company_id = int(self.data.get('company'))
                self.fields['department'].queryset = Department.objects.filter(company_id=company_id).order_by('name')
            except (ValueError, TypeError):
                pass  
        elif self.instance.pk:
            self.fields['department'].queryset = self.instance.company.department_set.order_by('name')

        if 'company' in self.data:
            try:
                company_id = int(self.data.get('company'))
                self.fields['employee'].queryset = Employee.objects.filter(company_id=company_id).order_by('name')
            except (ValueError, TypeError):
                pass  
        elif self.instance.pk:
            self.fields['employee'].queryset = self.instance.company.employee_set.order_by('name')

        




        # if 'department' in self.data:
        #     try:
        #         department_id = int(self.data.get('department'))
        #         self.fields['allocate_person'].queryset = Employee.objects.filter(department_id=department_id).order_by('name')
        #     except (ValueError, TypeError):
        #         pass  
        # elif self.instance.pk:
        #     self.fields['allocate_person'].queryset = self.instance.department.allocate_person_set.order_by('name')

        # if 'department' in self.data:
        #     try:
        #         department_id = int(self.data.get('department'))
        #         self.fields['allocate_person'].queryset = Employee.objects.filter(department_id=department_id).order_by('name')
        #     except (ValueError, TypeError):
        #         pass  
        # elif self.instance.pk:
        #     self.fields['allocate_person'].queryset = self.instance.department.allocate_person_set.order_by('name')


    # Validates the item Name Field
    #  def clean_code(self):
    #     code = self.cleaned_data.get('code')
    #     for instance in Item.objects.all():
    #         if instance.code == code:
    #             raise forms.ValidationError(name + ' is already exist')
    #     if (code == ""):
    #         raise forms.ValidationError('This field cannot be left blank')
    #     return code 





class ItemSearchForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['company','department', 'employee','item_type','item_name']

    def __init__(self, *args, **kwargs):
        super(ItemSearchForm, self).__init__(*args, **kwargs)
        self.fields['company'].required = False
        self.fields['department'].required = False
        self.fields['employee'].required = False
        self.fields['item_type'].required = False
        self.fields['item_name'].required = False
        self.fields['department'].queryset= Department.objects.none()
        self.fields['employee'].queryset = Employee.objects.none()

        if 'company' in self.data:
            try:
                company_id = int(self.data.get('company'))
                self.fields['department'].queryset = Department.objects.filter(company_id=company_id).order_by('name')
            except (ValueError, TypeError):
                pass  
        elif self.instance.pk:
            self.fields['department'].queryset = self.instance.company.department_set.order_by('name')

        if 'company' in self.data:
            try:
                company_id = int(self.data.get('company'))
                self.fields['employee'].queryset = Employee.objects.filter(company_id=company_id).order_by('name')
            except (ValueError, TypeError):
                pass  
        elif self.instance.pk:
            self.fields['employee'].queryset = self.instance.company.employee_set.order_by('name')


    
        






class EmployeeForm(forms.ModelForm):
    
    class Meta:
        model = Employee
        fields = ("employee_id","name","designation", "company", "department")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['department'].queryset= Department.objects.none()


        if 'company' in self.data:
            try:
                company_id = int(self.data.get('company'))
                self.fields['department'].queryset = Department.objects.filter(company_id=company_id).order_by('name')
            except (ValueError, TypeError):
                pass  
        elif self.instance.pk:
            self.fields['department'].queryset = self.instance.company.department_set.order_by('name')
       

    # Validates the item Name Field
    # def clean_emp_id(self):
    #     emp_id = self.cleaned_data.get('emp_id')
    #     for instance in Employee.objects.all():
    #         if instance.emp_id == emp_id:
    #             raise forms.ValidationError(emp_id + ' is already exist')
    #     if (emp_id == ""):
    #         raise forms.ValidationError('This field cannot be left blank')
    #     return emp_id





class EmployeeSearchForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employee_id','company','department' ,'name']

    def __init__(self, *args, **kwargs):
        super(EmployeeSearchForm, self).__init__(*args, **kwargs)
        self.fields['employee_id'].required = False
        self.fields['company'].required = False
        self.fields['department'].required = False
        self.fields['name'].required = False
        self.fields['department'].queryset= Department.objects.none()

        if 'company' in self.data:
            try:
                company_id = int(self.data.get('company'))
                self.fields['department'].queryset = Department.objects.filter(company_id=company_id).order_by('name')
            except (ValueError, TypeError):
                pass  
        elif self.instance.pk:
            self.fields['department'].queryset = self.instance.company.department_set.order_by('name')



class DepartmentForm(forms.ModelForm):
    
    class Meta:
        model = Department
        fields = ("company","name","short_name")

    # Validates the item Name Field
    # def clean_emp_id(self):
    #     emp_id = self.cleaned_data.get('emp_id')
    #     for instance in Employee.objects.all():
    #         if instance.emp_id == emp_id:
    #             raise forms.ValidationError(emp_id + ' is already exist')
    #     if (emp_id == ""):
    #         raise forms.ValidationError('This field cannot be left blank')
    #     return emp_id





class DepartmentSearchForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['company','name','short_name']

    def __init__(self,*args, **kwargs):
        super(DepartmentSearchForm, self).__init__(*args, **kwargs)
        self.fields['company'].required = False
