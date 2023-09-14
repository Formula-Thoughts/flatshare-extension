from dataclasses import dataclass
from typing import Protocol


class S3ObjectContent(Protocol):

    def read(self) -> str:
        ...


@dataclass(unsafe_hash=True)
class S3Object(Protocol):
    body: str = None


@dataclass(unsafe_hash=True)
class S3ObjectRef(Protocol):
    key: str = None


@dataclass(unsafe_hash=True)
class S3ObjectRefWrapper(Protocol):
    contents: S3ObjectRef = None


class S3ClientWrapper:

    def put_object(self,
                   bucket: str,
                   key: str,
                   body: str,
                   content_type: str) -> None:
        ...

    def list_objects_v2(self,
                        bucket: str,
                        prefix: str) -> list[S3ObjectRefWrapper]:
        ...

    def get_object(self,
                   bucket: str,
                   key: str) -> None:
        ...
