# On Windows, temporary file shold delete "after" storage was deleted
# NamedTemporaryFilePool ensures tempfile delete after tests.

from __future__ import annotations

import atexit
import gc
import os
import tempfile
import threading
from types import TracebackType
from typing import Any
from typing import IO


class NamedTemporaryFilePool:
    tempfile_pool: list[IO[Any]] = []
    lock = threading.Lock()

    def __new__(cls, **kwargs: Any) -> "NamedTemporaryFilePool":
        if not hasattr(cls, "_instance"):
            cls._instance = super(NamedTemporaryFilePool, cls).__new__(cls)
            atexit.register(cls._instance.cleanup)
        return cls._instance

    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs

    def tempfile(self) -> IO[Any]:
        self._tempfile = tempfile.NamedTemporaryFile(delete=False, **self.kwargs)
        with self.lock:
            self.tempfile_pool.append(self._tempfile)
        return self._tempfile

    def cleanup(self) -> None:
        with self.lock:
            gc.collect()
            for i in self.tempfile_pool:
                os.unlink(i.name)

    def __enter__(self) -> IO[Any]:
        return self.tempfile()

    def __exit__(
        self,
        exc_type: type[BaseException],
        exc_val: BaseException,
        exc_tb: TracebackType,
    ) -> None:
        self._tempfile.close()
