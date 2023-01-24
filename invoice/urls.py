from django.urls import path
from invoice import views

urlpatterns = [
    path('invoice/', views.invoice_list),
    path('invoice/<pk>', views.invoice_detail),
]