from dataclasses import dataclass
from datetime import datetime


@dataclass
class Optimization:
    id: str = None
    connector: str = ''
    campaign: str = ''
    target: float = 0
    margin: float = 0
    ad_cost: float = 0
    optimize: str = ''
    before: float = 0
    after: float = 0
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
