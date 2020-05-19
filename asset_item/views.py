from django.shortcuts import render, redirect
from .forms import CompanyForm, CompanySearchForm, ItemForm, ItemSearchForm, EmployeeForm, EmployeeSearchForm, DepartmentForm, DepartmentSearchForm,CreateUserForm
from .models import Company, Item, Employee, Department, Customer
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
import csv, io
from .resources import EmployeeResource
from django.contrib import messages
from tablib import Dataset
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only
import csv
#from .forms import CreateUserForm

# Create your views here.
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            
            group = Group.objects.get(name= 'customer')
            user.groups.add(group)
            Customer.objects.create(user=user)
            messages.success(request, 'Account was created for '+ username)
            return redirect('login')
    context = {'form': form}
    return render(request, 'register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')
    context = {}
    return render(request,'login.html', context)



def logoutUser(request):
    logout(request)
    return redirect('login')





@login_required(login_url='login')
def home(request):
    title = ""
    context = { "title": title}

    return render(request, 'home.html', context)


@login_required(login_url='login')
#@allowed_users(allowed_roles= ['admin'])
def company_entry(request):
    title = 'Add company'
    form = CompanyForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Saved')

        return redirect('/company_list')
    context = {
        "title": title, "form":form
    }

    return render(request,"company_entry.html", context)

@login_required(login_url='login')
#@allowed_users(allowed_roles= ['admin'])
def company_edit(request, pk):   
    instance = get_object_or_404(Company, id=pk)
    form = CompanyForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Succesfully Saved')
        return redirect('/company_list')
    context = {
            "title": 'Edit ' + str(instance.name),
            "instance": instance,
            "form": form,
        }
    return render(request, "company_entry.html", context)

@login_required(login_url='login')
#@allowed_users(allowed_roles= ['admin'])
def company_delete(request, pk):
    instance = get_object_or_404(Company, id=pk)
    instance.delete()
    return redirect('/company_list')

@login_required(login_url='login')
#@allowed_users(allowed_roles= ['customer','admin'])
def company_list(request):
     title = 'List of all company'
     queryset = Company.objects.all()
     form = CompanySearchForm(request.POST or None)
     context = {
         "title": title,
         "queryset": queryset,
         "form": form,
     }

     if request.method == 'POST':
            queryset = Company.objects.all().order_by('created_date').filter(name__icontains=form['name'].value(),short_name__icontains=form['short_name'].value())
            context = {
            "title": title,
            "queryset": queryset,
            "form": form,
            }

            if form['export_to_CSV'].value() == True:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="Company list.csv"'
                writer = csv.writer(response)
                writer.writerow(['COMPANY NAME', 'SHORT NAME', 'ADDRESS', 'PHONE', 'STATUS'])
                instance = queryset
                for row in instance:
                    writer.writerow([row.name, row.short_name, row.address, row.phone, row.status])
                return response
     return render(request, "company_list.html",context)


@login_required(login_url='login')
#@allowed_users(allowed_roles= ['admin','customer'])
def item_entry(request):
    title = 'Add Item'
    #allCompany = Company.objects.all()
    form = ItemForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Saved')

        return redirect('/item_list')
    context = {
        "title": title, "form":form
    }

    return render(request,'item_entry.html', context)
@login_required(login_url='login')
#@allowed_users(allowed_roles= ['admin'])
def item_edit(request, pk):
    
    instance = get_object_or_404(Item, id=pk)
    form = ItemForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Succesfully Saved')
        return redirect('/item_list')
    context = {
            "title": 'Edit ' + str(instance.item_name),
            "instance": instance,
            "form": form,
        }
    return render(request, "item_entry.html", context)    

def load_department(request):
    
    company_id = request.GET.get('company')
    departments= Department.objects.filter(company_id=company_id).order_by('name')
    context={'departments':departments}
    return render(request,'department_drop_down.html',context)


def load_employees(request):
    
    #company_id = request.GET.get('company')
    department_id =request.GET.get('department')
    employees = Employee.objects.filter(
        department_id=department_id).order_by('name')
    context={'employees':employees}
    return render(request,'employee_drop_down.html',context)

@login_required(login_url='login')
#@allowed_users(allowed_roles= ['customer','admin'])
def item_list(request):
    title = 'List of all item'
    queryset = Item.objects.all()
    form = ItemSearchForm(request.POST or None)
     #department = Department.objects.all()
    context = {
        "title": title,
        "queryset": queryset,
        "form": form,
        #'department':department
    }

    if request.method == 'POST':
        if form['company'].value() and form['department'].value() and form['employee'].value() and form['item_type'].value() and form['item_name'].value():
            queryset = Item.objects.all().filter(company_id=form['company'].value(),department_id=form['department'].value(),employee_id=form['employee'].value(),item_type__icontains=form['item_type'].value(),item_name__icontains=form['item_name'].value())
            context = {
            "title": title,
            "queryset": queryset,
            "form": form,
            }

        elif form['company'].value() and form['department'].value() and form['employee'].value() and form['item_type'].value():
            queryset = Item.objects.all().filter(company_id=form['company'].value(),department_id=form['department'].value(),employee_id=form['employee'].value(),item_type__icontains=form['item_type'].value())
            context = {
            "title": title,
            "queryset": queryset,
            "form": form,
            }
        elif form['company'].value() and form['department'].value()  and form['employee'].value():
            queryset = Item.objects.all().filter(company_id=form['company'].value(),department_id=form['department'].value(),employee_id=form['employee'].value())
            context = {
            "title": title,
            "queryset": queryset,
            "form": form,
            }
        elif form['company'].value() and form['department'].value():
            queryset = Item.objects.all().filter(company_id=form['company'].value(),department_id=form['department'].value())
            context = {
            "title": title,
            "queryset": queryset,
            "form": form,
            }

        elif form['company'].value() and form['employee'].value():
            queryset = Item.objects.all().filter(company_id=form['company'].value(),employee_id=form['employee'].value())
            context = {
            "title": title,
            "queryset": queryset,
            "form": form,
            }

        elif form['company'].value():
            queryset = Item.objects.all().filter(company_id=form['company'].value())
            context = {
            "title": title,
            "queryset": queryset,
            "form": form,
            }

        elif  form['department'].value():
            queryset = Item.objects.all().filter(department_id=form['department'].value())
            context = {
            "title": title,
            "queryset": queryset,
            "form": form,
            }
        
        elif  form['employee'].value():
            queryset = Item.objects.all().filter(employee_id=form['employee'].value())
            context = {
            "title": title,
            "queryset": queryset,
            "form": form,
            }
        elif form['item_type'].value():
            queryset = Item.objects.all().filter(item_type__icontains=form['item_type'].value())
            context = {
            "title": title,
            "queryset": queryset,
            "form": form,
            }
        else:
            queryset = Item.objects.all().filter(item_name__icontains=form['item_name'].value())
            context = {
            "title": title,
            "queryset": queryset,
            "form": form,
            }

            # if form['export_to_CSV'].value() == True:
            #     response = HttpResponse(content_type='text/csv')
            #     response['Content-Disposition'] = 'attachment; filename="Company list.csv"'
            #     writer = csv.writer(response)
            #     writer.writerow(['ITEM NAME', 'DESCRIPTION', 'ITEM TYPE', 'CODE', 'UNIT','COMPANY NAME','DEPARTMENT NAME', 'PURCHASE DATE', 'ALLOCATED PERSON'])
            #     instance = queryset
            #     for row in instance:
            #         writer.writerow([row.name, row.description, row.item_type, row.code, row.unit, row.company, row.department, row.purchase_date, row.allocate_person])
            #     return response
    return render(request, "item_list.html", context)


@login_required(login_url='login')
#@allowed_users(allowed_roles= ['admin'])
def item_delete(request, pk):
    instance = get_object_or_404(Item, id=pk)
    instance.delete()
    return redirect('/item_list')




@login_required(login_url='login')
#@allowed_users(allowed_roles= ['admin'])
def employee_entry(request):
    title = 'Add Employee'
    allEmployee = Employee.objects.all()
    form = EmployeeForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Saved')

        return redirect('/employee_list')
    context = {
        "title": title, "form":form, 'allEmployee': allEmployee
    }

    return render(request,'employee_entry.html', context)

def employee_upload(request):
    
    if request.method =="POST":
        company = Company.objects.all()
        department =Department.objects.all()
        emp = Employee.objects.filter(department=department,company=company)
        print(emp)
        employee_resource = EmployeeResource()
        dataset = Dataset()
        new_employee = request.FILES['myfile']
        if not new_employee.name.endswith('.xlsx'):
            messages.error(request, 'This is not a xlsx file')
            return render (request, 'employee_upload.html')
        imported_data = dataset.load(new_employee.read(), format='xlsx')
        print(imported_data)
        for data in imported_data:
            print(data[0])
            # emp = Employee(
            #     employee_id = data[0],
            #     name = data[1],
            #     designation = data[2],
            #     department = data[3],
            #     company = data[4]
            # )
            # emp.save()

    return render(request, 'employee_upload.html')



    # data_set = csv_files.read().decode('UTF-8')
    # io_string = io.StringIO(data_set)
    # next(io_string)
    # for column in csv.reader(io_string, delimiter=',', quotechar="|"):
    #     _,created = Employee.objects.update_or_create(
    #         employee_id = column[0],
    #         name =column[1],
    #         designation = column[2],
    #         department = column[3],
    #         company = column[4],

    #     )
    # context ={}
    # return render (request,template,context)



@login_required(login_url='login')
#@allowed_users(allowed_roles= ['admin'])
def employee_edit(request, pk):   
    instance = get_object_or_404(Employee, id=pk)
    form = EmployeeForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Succesfully Saved')
        return redirect('/employee_list')
    context = {
            "title": 'Edit ' + str(instance.employee_id),
            "instance": instance,
            "form": form,
        }
    return render(request, "employee_entry.html", context)    

@login_required(login_url='login')
#@allowed_users(allowed_roles= ['customer','admin'])
def employee_list(request):
    title = 'List of all employee'
    queryset = Employee.objects.all()
    form = EmployeeSearchForm(request.POST or None)
    context = {
        "title": title,
        "queryset": queryset,
        "form": form,
    }

     
    if request.method == 'POST':
        if form['employee_id'].value() and form['company'].value() and form['department'].value() and form['name'].value():
            queryset = Employee.objects.all().filter(employee_id__icontains=form['employee_id'].value(),company_id=form['company'].value(),department_id=form['department'].value(),name__icontains=form['name'].value())
            context = {
            "title": title,
            "queryset": queryset,
            "form": form,
            }
        elif form['employee_id'].value() and form['company'].value() and form['department'].value():
            queryset = Employee.objects.all().filter(employee_id__icontains=form['employee_id'].value(),company_id=form['company'].value(), department_id=form['department'].value())
            context = {
            "title": title,
            "queryset": queryset,
            "form": form,
            }
        elif form['employee_id'].value() and form['company'].value() :
            queryset = Employee.objects.all().filter(employee_id__icontains=form['employee_id'].value(),company_id=form['company'].value())
            context = {
            "title": title,
            "queryset": queryset,
            "form": form,
            }
        elif form['employee_id'].value():
            queryset = Employee.objects.all().filter(employee_id__icontains=form['employee_id'].value())
            context = {
            "title": title,
            "queryset": queryset,
            "form": form,
            }
        elif form['company'].value():
            queryset = Employee.objects.all().filter(company_id=form['company'].value())
            context = {
            "title": title,
            "queryset": queryset,
            "form": form,
            }

        elif form['department'].value():
            queryset = Employee.objects.all().filter(department_id=form['department'].value())
            context = {
            "title": title,
            "queryset": queryset,
            "form": form,
            }

        else:
            
            queryset = Employee.objects.all().filter(name__icontains=form['name'].value())
            context = {
            "title": title,
            "queryset": queryset,
            "form": form,
            }
    return render(request, "employee_list.html",context)


@login_required(login_url='login')
#@allowed_users(allowed_roles= ['admin'])
def employee_delete(request, pk):
    instance = get_object_or_404(Employee, id=pk)
    instance.delete()
    return redirect('/employee_list')



@login_required(login_url='login')
#@allowed_users(allowed_roles= ['admin'])
def department_entry(request):
    title = 'Add Department'
    form = DepartmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Saved')

        return redirect('/department_list')
    context = {
        "title": title, "form":form
    }

    return render(request,'department_entry.html', context)

@login_required(login_url='login')
#@allowed_users(allowed_roles= ['admin'])
def department_edit(request, pk):   
    instance = get_object_or_404(Department, id=pk)
    form = DepartmentForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Succesfully Saved')
        return redirect('/department_list')
    context = {
            "title": 'Edit ' + str(instance.name),
            "instance": instance,
            "form": form,
        }
    return render(request, "department_entry.html", context)

@login_required(login_url='login')
#@allowed_users(allowed_roles= ['admin'])
def department_delete(request, pk):
    instance = get_object_or_404(Department, id=pk)
    instance.delete()
    return redirect('/department_list')

@login_required(login_url='login')
#@allowed_users(allowed_roles= ['customer','admin'])
def department_list(request):
     title = 'List of all Department'
     queryset = Department.objects.all()
     form = DepartmentSearchForm(request.POST or None)
     context = {
         "title": title,
         "queryset": queryset,
         "form": form,
     }

     if request.method == 'POST':
            queryset = Department.objects.all().order_by('name').filter(short_name__icontains=form['short_name'].value())
            context = {
            "title": title,
            "queryset": queryset,
            "form": form,
            }

     if request.method == 'POST':
        if form['company'].value() and form['name'].value() and form['short_name'].value():
            queryset = Department.objects.all().filter(company_id=form['company'].value(),name__icontains=form['name'].value(),short_name__icontains=form['short_name'].value())
            context = {
            "title": title,
            "queryset": queryset,
            "form": form,
            }
        elif form['company'].value() and form['name'].value():
            queryset = Department.objects.all().filter(company_id=form['company'].value(),name__icontains=form['name'].value())
            context = {
            "title": title,
            "queryset": queryset,
            "form": form,
            }

        elif form['company'].value() and  form['short_name'].value():
            queryset = Department.objects.all().filter(company_id=form['company'].value(),short_name__icontains=form['short_name'].value())
            context = {
            "title": title,
            "queryset": queryset,
            "form": form,
            }

        elif form['company'].value():
            queryset = Department.objects.all().filter(company_id=form['company'].value())
            context = {
            "title": title,
            "queryset": queryset,
            "form": form,
            }
        elif  form['name'].value():
            queryset = Department.objects.all().filter(name__icontains=form['name'].value())
            context = {
            "title": title,
            "queryset": queryset,
            "form": form,
            }
        else:
            queryset = Department.objects.all().filter(short_name__icontains=form['short_name'].value())
            context = {
            "title": title,
            "queryset": queryset,
            "form": form,
            }

     return render(request, "department_list.html",context)
