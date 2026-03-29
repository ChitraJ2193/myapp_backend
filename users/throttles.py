from rest_framework.throttling import ScopedRateThrottle


class ScopedAuthThrottle(ScopedRateThrottle):
    """Use with `throttle_scope` on views (rates in REST_FRAMEWORK DEFAULT_THROTTLE_RATES)."""
