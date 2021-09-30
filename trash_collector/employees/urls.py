from django.urls import path
from . import views

# TODO: Determine what distinct pages are required for the user stories, add a path for each in urlpatterns

app_name = "employees"
urlpatterns = [
    path('', views.index, name="index"),
    path('create_employee/', views.create_employee, name="create_employee"),
    path('edit_employee_profile/', views.edit_employee_profile, name="edit_employee_profile"),
]
