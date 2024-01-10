# middleware.py
from django.utils import timezone
from .models import ActivityLog

class ActivityLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Log activity for authenticated users only
        if request.user.is_authenticated:
            log = ActivityLog(
                user=request.user,
                path=request.path,
                method=request.method,
                status_code=response.status_code,
                timestamp=timezone.now(),
            )
            log.save()

        return response