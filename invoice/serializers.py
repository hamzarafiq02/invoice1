from rest_framework import serializers
from invoice.models import Invoice

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ('id', 'name', 'description', 'total', 'paid', 'created')