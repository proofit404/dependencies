log = __builtins__["print"]


class Consul:
    """Service discovery client."""

    kv = {
        "postgresql_host": (
            ...,
            {"Value": "postgresql-instance1.cg034hpkmmjt.us-east-1.rds.amazonaws.com"},
        ),
        "postgresql_port": (..., {"Value": "5432"}),
        "redis_host": (..., {"Value": "redis-01.7abc2d.0001.usw2.cache.amazonaws.com"}),
        "redis_port": (..., {"Value": "6379"}),
    }

    def __init__(self):
        log("Connecting to local consul agent")
