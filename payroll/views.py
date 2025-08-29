import pandas as pd
from io import BytesIO
from django.http import FileResponse
from rest_framework.views import APIView, status
from rest_framework.response import Response
from .models import EmployeePayroll
from .serializers import EmployeePayrollSerializer
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


class UploadPayrollFile(APIView):
    def post(self,request):
        file_obj = request.FILES['file']
        df = pd.read_excel(file_obj)

        for _, row in df.iterrows():
            #BaseSalary + Bonus – Deductions
            try:
                net_salary = row['BaseSalary'] + row['Bonus'] - row['Deductions']
                EmployeePayroll.objects.update_or_create(employee_id=row['EmployeeID'],defaults={
                                    "name": row['Name'],
                                    "month" :row['Month'],
                                    "department":row["Department"],
                                    "base_salary": row["BaseSalary"],
                                    "bonus": row["Bonus"],
                                    "deductions": row["Deductions"],
                                    "net_salary": net_salary,
                                    })
            except Exception as err:
                print(err, "error")
            return Response({"Messege": "Payroll Data Uplaoded"}, status=201)
        
class PayrollSummery(APIView):
    def get(self,request,month):
        employees = EmployeePayroll.objects.filter(month=month)
        serializer = EmployeePayrollSerializer(employees, many=True)
        return Response(serializer.data)

class GeneratePayrollPDF(APIView):
    def get(self,request,month):
        employees = EmployeePayroll.objects.filter(month=month)
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)

        styles = getSampleStyleSheet()
        elements = [Paragraph(f"payroll report - {month}", styles['Title'])]

        data = [["Employee","Department","Base","Bonus","Deductions","Net"]]

        for emp in employees:
            data.append([emp.name,emp.department,str(emp.base_salary),str(emp.bonus),str(emp.deductions),str(emp.net_salary)])

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ]))
        elements.append(table)

        doc.build(elements)
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True,filename=f"Payroll_{month}.pdf")