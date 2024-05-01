from django.urls import path,include
from .views import VendorPerformanceView, AcknowledgePurchaseOrder,VendorViewSet,PurchaseOrderViewSet,HistoricalPerformanceViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'vendors', VendorViewSet)
router.register(r'purchase-orders', PurchaseOrderViewSet)
router.register(r'historical-performances', HistoricalPerformanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('vendors/<int:vendor_id>/performance/', VendorPerformanceView.as_view(), name='vendor_performance'),
    path('purchase-orders/<int:po_id>/acknowledge/', AcknowledgePurchaseOrder.as_view(), name='acknowledge_purchase_order'),
]
