from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.

from .models import *
#from .forms import CompanyForm


# class CompanyAdmin(admin.ModelAdmin):
#     list_display = ["name","short_name", "address","created_by","modified_by","status"]
#     form = CompanyForm
#     list_filter = ["short_name"]
#     search_fields = ["short_name"]


# class ItemAdmin(admin.ModelAdmin):
#     list_display = ["name","description", "item_type","code","unit","purchase_date", "employee","created_by","modified_by","created_date","modified_date"]
#     form = ItemForm
#     list_filter = ["item_type"]
#     search_fields = ["code"]
    

# admin.site.register(Company,CompanyAdmin)
# #admin.site.register(Item,ItemAdmin)
# admin.site.register(Customer)
#admin.site.register(Employee)

@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    list_display =('employee_id', 'name','designation','department', 'company')
