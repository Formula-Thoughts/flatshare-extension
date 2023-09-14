import uuid
from dataclasses import dataclass, field
from datetime import datetime


def uuid4_str():
    return str(uuid.uuid4())


@dataclass(unsafe_hash=True)
class Resource:
    id: str = field(default_factory=uuid4_str)


@dataclass(unsafe_hash=True)
class DataModel(Resource):
    created: datetime = field(default_factory=datetime.utcnow)


@dataclass(unsafe_hash=True)
class Group(DataModel):
    name: str = None
    code: int = None