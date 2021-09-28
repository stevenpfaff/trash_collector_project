from django.db.models.manager import EmptyManager
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Employee
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.

@login_required
def index(request):
    logged_in_user = request.user
    try: 
        logged_in_employee = Employee.objects.get(user=logged_in_user)
        context = {
            'logged_in_employee': logged_in_employee
    }
    # This line will get the Customer model from the other app, it can now be used to query the db for Customers
        Customer = apps.get_model('customers.Customer')
        return render(request, 'employees/index.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))
    
    
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