from dataclasses import dataclass


log = __builtins__["print"]


@dataclass
class App:
    """Service object."""

    database: "PostgreSQL"
    cache: "Redis"

    def run(self):
        """Run business transaction."""
        self.database.connect()
        self.cache.connect()


@dataclass
class PostgreSQL:
    """PostgreSQL client."""

    host: str
    port: int

    def connect(self):
        """Open connection."""
        log(f"Connecting to {self.host}:{self.port}")


@dataclass
class Redis:
    """Redis client."""

    host: str
    port: int

    def connect(self):
        """Open connection."""
        log(f"Connecting to {self.host}:{self.port}")
