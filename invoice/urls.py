from django.urls import path
from invoice import views
from .views import *

urlpatterns = [
    path('invoice/', views.invoice_list),
    path('invoice/<pk>', views.invoice_detail),
    path('pdf/<pk>', Genratepdf.as_view()),
    path('send-email/', send_email_view, name='send-email'),
]