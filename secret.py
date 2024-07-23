from typing import Any


class Secret:
    def __init__(self, secret_str: str = None):
        if isinstance(secret_str, Secret):
            self._secret_str = secret_str._secret_str
        else:
            self._secret_str = secret_str

    def get_secret_string(self) -> str:
        return self._secret_str

    def __eq__(self, other: Any) -> bool:
        return ((isinstance(other, str) and self._secret_str == other) or
                (isinstance(other, self.__class__) and self._secret_str == other._secret_str))

    def __str__(self) -> str:
        return '**********' if self._secret_str else ''

    def __hash__(self) -> int:
        return hash(self._secret_str)

    def __repr__(self) -> str:
        return f"secret('{self}')"

    def __len__(self) -> int:
        if self._secret_str:
            return len(self._secret_str)
        else:
            return 0
