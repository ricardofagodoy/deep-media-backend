from dataclasses import dataclass
from typing import Any
from models.base_model import BaseModel


@dataclass
class Connector(BaseModel):
    type: str
    configuration: Any
    options: Any
