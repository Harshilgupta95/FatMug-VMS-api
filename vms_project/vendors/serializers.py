from rest_framework import serializers
from .models import Vendor, PurchaseOrder, HistoricalPerformance

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

    def validate_vendor_code(self, value):
        # Ensure vendor code is unique
        if Vendor.objects.filter(vendor_code=value).exists():
            raise serializers.ValidationError("Vendor code must be unique.")
        return value

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

    def validate(self, data):
        # Ensure delivery date is after order date
        if data.get('delivery_date') < data.get('order_date'):
            raise serializers.ValidationError("Delivery date must be after order date.")
        return data

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'
