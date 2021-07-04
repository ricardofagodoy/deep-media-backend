import dataclasses
from abc import ABC
from dataclasses import dataclass


@dataclass
class BaseModel(ABC):

    @classmethod
    def from_dict(cls, dict_):
        class_fields = {f.name for f in dataclasses.fields(cls)}
        return cls(**{k: v for k, v in dict_.items() if k in class_fields})

    def to_dict(self):
        class_fields = {f.name for f in dataclasses.fields(self)}
        return {f: getattr(self, f) for f in class_fields}
