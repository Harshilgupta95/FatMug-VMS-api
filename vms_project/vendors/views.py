
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .backend_logics import calculate_on_time_delivery_rate, calculate_quality_rating_avg, calculate_average_response_time, calculate_fulfillment_rate
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from django.utils import timezone
from rest_framework import viewsets,status
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class HistoricalPerformanceViewSet(viewsets.ModelViewSet):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer

class VendorPerformanceView(APIView):
    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
            performance_data = {
                'on_time_delivery_rate': calculate_on_time_delivery_rate(vendor),
                'quality_rating_avg': calculate_quality_rating_avg(vendor),
                'average_response_time': calculate_average_response_time(vendor),
                'fulfillment_rate': calculate_fulfillment_rate(vendor)
            }
            return Response(performance_data, status=status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)

class AcknowledgePurchaseOrder(APIView):
    def post(self, request, po_id):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
            purchase_order.acknowledgment_date = timezone.now()
            purchase_order.status='completed'
            purchase_order.save()
            # Recalculate average_response_time
            vendor = purchase_order.vendor
            vendor.average_response_time = calculate_average_response_time(vendor)
            vendor.save()
            return Response({'message': 'Purchase Order acknowledged successfully'}, status=status.HTTP_200_OK)
        except PurchaseOrder.DoesNotExist:
            return Response({'error': 'Purchase Order not found'}, status=status.HTTP_404_NOT_FOUND)
