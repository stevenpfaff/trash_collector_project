from django.db.models.manager import EmptyManager
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Employee
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
import calendar
# Create your views here.
# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.

@login_required
def index(request):
    logged_in_user = request.user
    # This line will get the Customer model from the other app, it can now be used to query the db for Customers
    Customer = apps.get_model('customers.Customer')
    try: 
        logged_in_employee = Employee.objects.get(user=logged_in_user)
        today = date.today()
        print(calendar.day_name[today.weekday()])
    

        customers_in_zipcodes = Customer.objects.filter(zip_code=logged_in_employee.zip_code)
        todays_customer_pickups = customers_in_zipcodes.filter(one_time_pickup=today) | customers_in_zipcodes.filter(weekly_pickup=today)
        non_suspended_accounts = todays_customer_pickups.filter(suspend_start=today) | todays_customer_pickups.filter(suspend_end=today)
        picked_up_trash = non_suspended_accounts.filter(date_of_last_pickup = today)
        if picked_up_trash == False:
            return 

        context = {
            'logged_in_employee': logged_in_employee,
            'today' : today
    }
        return render(request, 'employees/index.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create_employee'))
    
    
@login_required
def create_employee(request):
    logged_in_user = request.user
    if request.method == "POST":
        name = request.POST.get('name')
        zip_code = request.POST.get('zip_code')
        new_employee = Employee(name=name, zip_code=zip_code, user=logged_in_user)
        new_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        return render(request, 'employees/create_employee.html')

@login_required
def edit_employee_profile(request, employee_id):
    logged_in_employee = Employee.objects.get(pk=employee_id)
    if request.method == "POST":
        logged_in_employee.name = request.POST.get('name')
        logged_in_employee.zip_code = request.POST.get('zip_code')
        logged_in_employee.save()
        return HttpResponseRedirect(reverse('employee:index'))
    else:
        context = {
            'logged_in_employee': logged_in_employee
        }
        return render(request, 'employees/edit_employee_profile.html', context)