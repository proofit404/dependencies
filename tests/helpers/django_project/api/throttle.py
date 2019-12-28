from rest_framework.throttling import BaseThrottle
from rest_framework.throttling import ScopedRateThrottle


class _ThrottleEveryOne(BaseThrottle):
    def allow_request(self, request, view):
        return False


class _ThrottleDefaultScope(ScopedRateThrottle):
    THROTTLE_RATES = {"throttle_scope": "1/min"}

    def wait(self):
        return 1


class _ThrottleCustomScope(ScopedRateThrottle):
    THROTTLE_RATES = {"custom_scope": "1/min"}
    scope_attr = "custom_throttle_scope"

    def wait(self):
        return 1
