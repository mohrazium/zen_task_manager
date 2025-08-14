from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from returns.result import Result  # Assume you have an Either[L, R]

from src.config.exceptions.failure_exception import \
    FailureException  # Your custom exception

T = TypeVar("T")  # Return type
P = TypeVar("P")  # Param type

class Usecase(Generic[T, P], ABC):
    @abstractmethod
    async def call(self, params: P) -> Result[FailureException, T]:
        pass