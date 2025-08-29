from django.db import models

class EmployeePayroll(models.Model):
    employee_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=30)
    department = models.CharField(max_length=30)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.CharField(max_length=10)
