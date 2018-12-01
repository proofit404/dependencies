from rest_framework.throttling import BaseThrottle


class ThrottleEveryOne(BaseThrottle):
    def allow_request(self, request, view):
        return False
