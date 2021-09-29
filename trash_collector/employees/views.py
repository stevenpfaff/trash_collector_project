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
# Create your views here.
# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.

@login_required
def index(request):
    logged_in_user = request.user
    try: 
        logged_in_employee = Employee.objects.get(user=logged_in_user)
        today = date.today()
        context = {
            'logged_in_employee': logged_in_employee,
            'today' : today
    }
    # This line will get the Customer model from the other app, it can now be used to query the db for Customers
        Customer = apps.get_model('customers.Customer')
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


class MatchingZipView(generic.ListView):
    model = Employee
    template_name = 'employees/matching_zip.html'
    context_object_name = 'matching_zip'
    def get_queryset(self):
        Customer = apps.get_model('customers.Customer')
        self.employee_zip = get_object_or_404(Customer, name=self.kwargs['customers'])
        return Employee.objects.filter(customer=self.employee_zip)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer_zip_code'] = self.employee_zip.zip_code
        return context