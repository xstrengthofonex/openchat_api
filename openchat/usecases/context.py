from dataclasses import dataclass

from openchat.repositories.in_memory_repositories import InMemoryRepository
from openchat.usecases.repositories import Repository


@dataclass(frozen=True)
class Context:
    repository: Repository


context = Context(repository=InMemoryRepository())
