# Classes for generating different types of red-teaming contexts for the prompt
from abc import ABC, abstractmethod


def get_context_names(contexts: list) -> list:
    return [context.get_context_name() for context in contexts]


class Context(ABC):

    @abstractmethod
    def get_context(self, problem: str, prefix: str = "", suffix: str = "", index: int = 0) -> str:
        pass

    def get_context_name(self) -> str:
        return self.__class__.__name__
