from datetime import datetime
from django.http import HttpResponseNotFound

class ShutdownMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_date = datetime.now()
        shutdown_date = datetime(2024, 12, 12)
        if current_date > shutdown_date:
            return HttpResponseNotFound("Сайт закрыт")
        else:
            return self.get_response(request)