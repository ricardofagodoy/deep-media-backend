import uuid
from dataclasses import dataclass
from models.base_model import BaseModel


@dataclass
class Configuration(BaseModel):
    type: str
    name: str
    ads_account: str
    ads_campaign: str
    adcost_target: float
    ga_account: str
    ga_property: str
    ga_profile: str
    ga_dimension: str
    ga_metric: str
    active: bool
    id: str = uuid.uuid4().hex
