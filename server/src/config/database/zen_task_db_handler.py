

from src.config.database.zen_task_db import ZenTaskDatabase


_db = ZenTaskDatabase()
_db.initialize()


class ZenTaskDbHandler:
    def __init__(self) -> None:
        pass

    @staticmethod
    def db() -> ZenTaskDatabase:
        return _db
