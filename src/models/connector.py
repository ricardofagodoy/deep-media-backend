from dataclasses import dataclass
from typing import Any


@dataclass
class Connector:
    type: str
    configuration: Any
    options: Any

    def to_dict(self):
        return {
            'type': self.type,
            'configuration': self.configuration,
            'options': self.options
        }
