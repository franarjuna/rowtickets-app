from rest_framework import viewsets

class CronViewSet(viewsets.ViewSet):
    def list(self, request):
        print("test")