from typing import Protocol, ContextManager

class TransactionManagerInterface(Protocol):
    def transaction(self) -> ContextManager: ...