from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin


class BlockIPMiddleware(MiddlewareMixin):
    """
    Middleware to block specific IP addresses from accessing the site
    """
    blocked_ips = ['103.61.103.162']  # Add IPs to block here
    
    def process_request(self, request):
        if request.META.get('REMOTE_ADDR') in self.blocked_ips:
            return HttpResponseForbidden("You are restricted to access the site.")
        return None

