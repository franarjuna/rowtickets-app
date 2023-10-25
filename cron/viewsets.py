from rest_framework import viewsets
from rest_framework.response import Response
from orders.models import Order
from datetime import datetime, timedelta
from django.utils import timezone

class CronViewSet(viewsets.ViewSet):
    def list(self, request):
        time_threshold = datetime.now() - timedelta(hours=5)
        newquery = Order.objects.filter(status = 'in_progress', created__lt = time_threshold ).all()
        total = newquery.count()  # Get the count of canceled orders

        # Update the status for all matching orders
        newquery.update(status='cancelled')
        
        return Response({'total':total})