from typing import List
from connectors.base_connector import BaseConnector
from models.optimization import Optimization
from repository.store_repository import StoreRepository
import datetime


class OptimizerService:
    _MARGIN = 0.005

    def __init__(self, repository: StoreRepository, connectors: List[BaseConnector]):
        self.repository = repository
        self.connectors = {conn.type: conn for conn in connectors}

    def optimize(self, connector_type: str, uid):

        connector_handler = self.connectors.get(connector_type)

        if not connector_handler:
            raise Exception('Handler to %s not configured' % connector_type)

        # Load connector and configurations from repository
        connector_configuration = self.repository.load_connector(connector_type, uid).configuration
        configurations = [
            conf for conf in self.repository.load_configurations(uid) if conf.type == connector_type and conf.active
        ]

        current_date = datetime.datetime.now()

        # Optimize each campaign
        for configuration in configurations:
            margin = self._MARGIN
            adcost_target = configuration.adcost_target/100

            # Pull adcost
            ad_cost = connector_handler.load_adcost(connector_configuration, configuration, current_date)
            before = 15
            optimize = 'CPA'

            # Calculate optimization
            optimization = self.optimize_roas(margin, adcost_target, ad_cost)

            # TODO: CALL API TO CHANGE CAMPAIGN
            after = before * (1 + optimization)

            optimization = Optimization(
                connector_type,
                configuration.ads_campaign,
                adcost_target,
                margin,
                ad_cost,
                optimize,
                before,
                after
            )

            self.repository.persist_optimization(optimization, uid)

    @staticmethod
    def optimize_roas(margin: float, adCostMeta: float, adCostDia: float, adCostOntem: float = None) -> float:

        def diff(adCost):
            return round(adCostMeta - adCost, 4)

        # Input error
        if not all([margin, adCostMeta, adCostDia]):
            return 0

        # Small diff today, don't act
        diff_adcost = diff(adCostDia)

        if abs(diff_adcost) <= margin:
            return 0

        # Optimization ratio
        opt_ratio = diff_adcost * 10

        # Boost 0.1% over default optimization for each 1% diff yesterday
        if adCostOntem:
            diff_boost = diff(adCostOntem)

            if diff_boost * opt_ratio > 0:
                opt_ratio += diff_boost

        return round(opt_ratio, 4)
