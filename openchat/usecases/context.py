from dataclasses import dataclass

from openchat.repositories.in_memory_repositories import InMemoryRepository
from openchat.usecases.repositories import Repository


@dataclass
class Context:
    repository: Repository = None

    def initialize(self):
        self.repository = InMemoryRepository()


usecase_context = Context()
usecase_context.initialize()
