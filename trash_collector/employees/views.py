from django.db.models.manager import EmptyManager
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Employee
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
from django.views import generic
from django.shortcuts import get_object_or_404
# Create your views here.
# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.

@login_required
def index(request):
    logged_in_user = request.user
    Customer = apps.get_model('customers.Customer')
    try: 
        logged_in_employee = Employee.objects.get(user=logged_in_user)
        today = date.today()
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday_num = today.weekday()
        specific_day = weekdays[weekday_num]
        
        
        # find out how to get day of week in python (will be an integer)
        # create a list of the days that match up to the integers
        # use the interger as the index to the the string of the current day!
        # 0 = 'Monday'
        # 1 = 'Tuesday'
        customers_in_zipcode = Customer.objects.filter(zip_code=logged_in_employee.zip_code)
        todays_customer_pickup = customers_in_zipcode.filter(one_time_pickup=today) | customers_in_zipcode.filter(weekly_pickup=specific_day)
        non_suspended_accounts = todays_customer_pickup.filter(suspend_starttoday) | todays_customer_pickup.filter(suspend_end=today)
        picked_up_trash = todays_customer_pickup.filter(date_of_last_pickup=today)
        if non_suspended_accounts == False & picked_up_trash == False:
            return 
        

        context = {
            'logged_in_employee': logged_in_employee,
            'today' : today
    }
    # This line will get the Customer model from the other app, it can now be used to query the db for Customers
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
def edit_employee_profile(request):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        logged_in_employee.name = name_from_form
        logged_in_employee.address = address_from_form
        logged_in_employee.zip_code = zip_from_form
        logged_in_employee.save()
        return HttpResponseRedirect(reverse('employee:index'))
    else:
        context = {
            'logged_in_employee': logged_in_employee
        }
        return render(request, 'employees/edit_employee_profile.html', context)





