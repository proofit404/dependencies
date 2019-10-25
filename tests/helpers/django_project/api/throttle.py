from rest_framework.throttling import BaseThrottle, ScopedRateThrottle


class ThrottleEveryOne(BaseThrottle):
    def allow_request(self, request, view):
        return False


class ThrottleEveryOneInScope(ScopedRateThrottle):
    scope = 'throttle_scope'

    def allow_request(self, request, view):
        return False
