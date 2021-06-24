from dataclasses import dataclass
from datetime import datetime


@dataclass
class Optimization:
    id: str
    connector: str
    date: datetime
    campaign: str
    campaign_id: str
    target: float
    margin: float
    ad_cost: float
    optimize: str
    before: float
    after: float

    @staticmethod
    def format_datetime(value: datetime):
        return value.strftime('%d/%m/%Y %H:%M') if value else None

    def to_dict(self):
        return {
            'id': self.id,
            'connector': self.connector,
            'campaign': self.campaign,
            'campaign_id': self.campaign_id,
            'target': self.target,
            'margin': self.margin,
            'ad_cost': self.ad_cost,
            'optimize': self.optimize,
            'before': self.before,
            'after': self.after,
            'date': self.format_datetime(self.date)
        }
