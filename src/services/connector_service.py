from datetime import datetime, timedelta
from typing import List, Any
from pytz import timezone
from connectors.base_connector import BaseConnector
from models.configuration import Configuration
from models.connector import Connector
from models.optimization import Optimization
from repository.job_repository import JobRepository
from repository.store_repository import StoreRepository

DEFAULT_TIMEZONE = 'America/Sao_Paulo'


class ConnectorService:

    def __init__(self, repository: StoreRepository, job_repository: JobRepository, connectors: List[BaseConnector]):
        self.repository = repository
        self.job_repository = job_repository
        self.connectors = {conn.type: conn for conn in connectors}

    def get_connector_options(self, connector_type, uid) -> Any:

        connector = self.repository.load_connector(connector_type, uid)

        if not connector:
            raise Exception('Connector %s not configured' % connector_type)

        return connector.options

    def delete_connector(self, connector_type, uid) -> Any:

        # Delete job scheduled for this connector
        self.job_repository.delete_scheduled_optimization(connector_type, uid)

        # Wipe all connector settings
        self.repository.delete_connector(connector_type, uid)

        # Finally, remove all configurations related to this connector
        configurations = self.repository.load_configurations(uid)

        for configuration in configurations:
            if configuration.type == connector_type:
                self.repository.delete_configuration(configuration.id, uid)

    def refresh_connector(self, connector_type, uid):

        connector_handler = self.connectors.get(connector_type)

        if not connector_handler:
            raise Exception('Connector %s not available' % connector_type)

        connector = self.repository.load_connector(connector_type, uid)

        if not connector:
            raise Exception('Connector %s not configured' % connector_type)

        # Update options
        connector.options = connector_handler.load_options(connector.configuration)

        self.repository.persist_connector(connector, uid)

    def configure_connector(self, connector_type, connector_configuration, uid) -> Connector:

        connector_handler = self.connectors.get(connector_type)

        if not connector_handler:
            raise Exception('Connector %s not available' % connector_type)

        # Build connector
        connector = connector_handler.build_connector(connector_configuration)

        # Create job to perform optimizations
        self.job_repository.schedule_optimization(connector_type, uid)

        return self.repository.persist_connector(connector, uid)

    def get_user_connectors(self, uid) -> List[str]:
        return self.repository.load_connectors(uid)

    def set_configuration(self, configuration: Configuration, uid) -> Configuration:
        return self.repository.persist_configuration(configuration, uid)

    def delete_configuration(self, configuration_id, uid):
        return self.repository.delete_configuration(configuration_id, uid)

    def get_configurations(self, uid) -> List[Configuration]:
        return self.repository.load_configurations(uid)

    def get_optimizations(self, uid) -> List[Optimization]:
        return self.repository.load_optimizations(uid)

    def get_future_optimizations(self, uid):
        jobs = self.job_repository.get_scheduled_optimizations(uid)
        return [{
            'next_run': job['next_run'],
            'type': job['type']
        } for job in jobs if job['uid'] == uid]

    def get_performance(self, configuration_id, uid):

        today = datetime.today().astimezone(timezone(DEFAULT_TIMEZONE)).replace(hour=0, minute=0, second=0)
        yesterday = today - timedelta(days=1)

        optimizations = self.repository.load_optimizations(uid, yesterday, configuration_id=configuration_id)

        # Format today to compare
        today = Optimization.format_datetime(today)

        return {
            'today': [o for o in optimizations if o.date >= today],
            'yeserday': [o for o in optimizations if o.date < today],
            'week': [],  # Not implemented yet
            'month': []  # Not implemented yet
        }
