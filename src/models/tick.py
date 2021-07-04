from dataclasses import dataclass, field
from datetime import datetime
from models.base_model import BaseModel


@dataclass
class Tick(BaseModel):
    date: datetime
    target: float
    value: float
