from django.db import models
from datetime import datetime, date

from django.urls import reverse 
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, null = True, on_delete = models.CASCADE)
    name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user




class Company(models.Model):
    # company_choice = ( ('Dekko Isho','Dekko Isho'), 
    # ('Dekko Accesories Limited', 'Dekko Accesories Limited') )


    
    name = models.CharField(max_length=255,blank=True ) #choices= company_choice
    
    short_name = models.CharField(max_length=255,blank=True)
    address = models.CharField(max_length=255,blank=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    modified_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=False,blank=True, null=True)
    modified_date = models.DateField(auto_now=True,blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    export_to_CSV = models.BooleanField(default =False)

    def __str__(self):
        return self.name
    



class Department(models.Model):
    company = models.ForeignKey(Company, on_delete = models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    short_name = models.CharField(max_length=255, blank=True, null=True)  
    created_by = models.IntegerField(blank=True, null=True)
    modified_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True,blank=True, null=True)

    def __str__(self):
        return self.name
    







class Employee(models.Model):
    employee_id = models.CharField(unique=True,max_length=255,blank =True)
    name = models.CharField(max_length=255,blank =True)
    designation = models.CharField(max_length=255, blank=True, null=True)
    
    created_by = models.IntegerField(blank=True, null=True)
    modified_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    company = models.ForeignKey(Company,on_delete = models.CASCADE)
    department = models.ForeignKey(Department, on_delete = models.CASCADE)
    

    def __str__(self):
        return self.name
    




class Item(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    item_name = models.CharField(max_length=255, blank =True)
    description = models.CharField(max_length=255, blank=True, null=True)
    item_choice = ( ('IT','IT'), 
    ('Electronics', 'Electronics') )
    item_type = models.CharField(max_length=255, blank =True, choices = item_choice )
    code = models.CharField(unique=True, max_length=255)
    unit = models.CharField(max_length=255, blank=True, null=True)
    purchase_date = models.DateField("Purchase Date",auto_now_add= False, auto_now = False,blank = True, null= True)
    #timestamp = models.DateField(auto_now=False, auto_now_add=False, blank = True)
    timestamp = models.DateField(auto_now_add=True, auto_now=False)
    created_by = models.IntegerField(blank=True, null=True)
    modified_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True,blank=True, null=True)
    export_to_CSV = models.BooleanField(default =False)
    
    company = models.ForeignKey(Company, on_delete = models.SET_NULL, null =True,blank=True)
    department = models.ForeignKey(Department, on_delete = models.SET_NULL,null= True, blank=True)
    employee = models.ForeignKey(Employee, on_delete = models.CASCADE, blank=True,  null=True)

    def __str__(self):
        return self.name
    

