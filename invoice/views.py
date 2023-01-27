from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .helpers import save_pdf
import datetime
from invoice.models import Invoice
from invoice.serializers import InvoiceSerializer
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from django.core.mail import send_mail
from account.models import User

 

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def invoice_list(request):
    if request.method == 'GET':
        invoices = Invoice.objects.all()
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = InvoiceSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def invoice_detail(request, pk):
    try:
        invoice = Invoice.objects.get(pk=pk)
    except Invoice.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = InvoiceSerializer(invoice, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        invoice.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)








class Genratepdf(APIView):
    @permission_classes([permissions.IsAuthenticated])
    def get(self, request, pk):
        invoice_objs = Invoice.objects.get(pk=pk)
        params = {
            'today': datetime.date.today(),
            'invoice_objs': invoice_objs
        }
        file_name , status = save_pdf(params)
        print(file_name)

        if not status:
            return Response({'status': 400})


        return Response({'status': 200 , 'path': f'/media/{file_name}.pdf'})




@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def send_email_view(request):
    invoice_pdf = Invoice.objects.get()
    params = {
            'today': datetime.date.today(),
            'invoice_objs': invoice_pdf
        }
    file_name , status = save_pdf(params)
    print(file_name)
    if not status:
            return Response({'status': 400})
            

    print(invoice_pdf)
    # Subject and message of the email
    path =  f'/media/{file_name}.pdf'
    print(path)
    link = 'http://127.0.0.1:8000'+path
    subject = 'Welcome to My Site'
    message = 'Thank you for visiting!, Here is your invoice Link '+link

    # Sender and recipient email addressess
    from_email = 'hamza99tech@gmail.com'
    to_email = request.user.email

    # Send the email
    send_mail(subject, message, from_email, [to_email], fail_silently=False)

    return Response({'message': 'Email sent successfully'})