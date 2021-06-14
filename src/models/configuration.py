from dataclasses import dataclass


@dataclass
class Configuration:
    type: str
    name: str
    ads_account: str
    ads_campaign: str
    adcost_target: float
    ga_account: str
    ga_property: str
    ga_metric: str
    active: bool
    id: str = None

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'ads_account': self.ads_account,
            'ads_campaign': self.ads_campaign,
            'adcost_target': self.adcost_target,
            'ga_account': self.ga_account,
            'ga_property': self.ga_property,
            'ga_metric': self.ga_metric,
            'active': self.active
        }
