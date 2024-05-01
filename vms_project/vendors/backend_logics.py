from django.db.models import Count, Avg
from django.utils import timezone
from .models import PurchaseOrder

def calculate_on_time_delivery_rate(vendor):
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    on_time_deliveries = completed_pos.filter(delivery_date__lte=timezone.now()).count()
    total_completed_pos = completed_pos.count()
    if total_completed_pos == 0:
        return 0
    return (on_time_deliveries / total_completed_pos) * 100

def calculate_quality_rating_avg(vendor):
    completed_pos_with_rating = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
    return completed_pos_with_rating.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0


def calculate_average_response_time(vendor):
    completed_pos_with_acknowledgment = PurchaseOrder.objects.filter(vendor=vendor, status='completed', acknowledgment_date__isnull=False)
    if completed_pos_with_acknowledgment.exists():
        response_times = [(po.acknowledgment_date - po.issue_date).total_seconds() for po in completed_pos_with_acknowledgment]
        return sum(response_times) / len(response_times)
    return 0

def calculate_fulfillment_rate(vendor):
    total_pos = PurchaseOrder.objects.filter(vendor=vendor)
    completed_pos = total_pos.filter(status='completed')
    successful_pos = completed_pos.exclude(quality_rating__lt=0).exclude(acknowledgment_date__isnull=True)
    if total_pos.exists():
        return (successful_pos.count() / total_pos.count()) * 100
    return 0
