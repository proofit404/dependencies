from rest_framework.throttling import BaseThrottle
from rest_framework.throttling import ScopedRateThrottle


class ThrottleEveryOne(BaseThrottle):
    def allow_request(self, request, view):
        return False


class ThrottleScope(ScopedRateThrottle):
    scope = "throttle_scope"

    def wait(self):
        return 1
