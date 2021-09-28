from django.db import models

# Create your models here.

# TODO: Create an Employee model with properties required by the user stories

class Employee(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey('accounts.User', blank=True, null=True, on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=5)
    customer = models.ForeignKey('customer.Customer', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name