from django.urls import path
from .views import UploadPayrollFile, PayrollSummery, GeneratePayrollPDF

urlpatterns = [
    path('upload/',UploadPayrollFile.as_view(),name="upload_payroll"),
    path('summary/<str:month>/', PayrollSummery.as_view(),name="payroll_summery"),
    path('pdf/<str:month>/',GeneratePayrollPDF.as_view(), name="payroll_pdf")
]