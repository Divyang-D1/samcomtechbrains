from rest_framework import serializers
from .models import EmployeePayroll


class EmployeePayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeePayroll
        fields = '__all__'