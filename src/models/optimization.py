from dataclasses import dataclass
from datetime import datetime
from models.base_model import BaseModel


@dataclass
class Optimization(BaseModel):
    id: str
    connector: str
    date: datetime
    account: str
    campaign: str
    target: float
    ad_cost: float
    optimize: str
    before: float
    after: float
