log = __builtins__["print"]


class Connection:
    """Manage connection."""

    def connect(self):
        """Perform database query."""
        log("CONNECT TO production;")

    def disconnect(self):
        """Perform database query."""
        log("DISCONNECT FROM production;")


class Cursor:
    """Manage cursor."""

    def __init__(self, connection):
        ...

    def begin_transaction(self):
        """Perform database query."""
        log("BEGIN TRANSACTION;")

    def commit_transaction(self):
        """Perform database query."""
        log("COMMIT TRANSACTION;")

    def select(self, **kwargs):
        """Perform database query."""
        log("SELECT * FROM users FOR UPDATE;")
        return self

    def delete(self):
        """Perform database query."""
        log("DELETE FROM users;")
