from dataclasses import dataclass, field


@dataclass
class Request:
    method: str
    url: str
    protocol: str
    headers: dict = field(default_factory=dict)
    content: bytes = b''


@dataclass
class Response:
    status: int
    detail: str
    headers: dict = field(default_factory=dict)
    content: bytes = b''
