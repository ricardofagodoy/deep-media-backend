from dataclasses import dataclass
from datetime import datetime


@dataclass
class Optimization:
    connector: str
    campaign: str
    target: float
    margin: float
    ad_cost: float
    optimize: str
    before: float
    after: float
    id: str = None
    date: datetime = datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'connector': self.connector,
            'campaign': self.campaign,
            'target': self.target,
            'margin': self.margin,
            'ad_cost': self.ad_cost,
            'optimize': self.optimize,
            'before': self.before,
            'after': self.after,
            'date': self.date.strftime('%d/%m/%Y %H:%M') if self.date else None
        }
