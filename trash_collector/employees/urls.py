from django.urls import path

from . import views

# TODO: Determine what distinct pages are required for the user stories, add a path for each in urlpatterns

app_name = "employees"
urlpatterns = [
    path('', views.index, name="index"),
    path('edit_employee/', views.edit_employee, name="edit_employee"),
    path('edit_profile/', views.edit_employee_profile, name="edit_employee_profile"),
]