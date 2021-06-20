import os
import random
import logging
import firebase_admin
from firebase_admin import auth
from flask import Flask
from flask_expects_json import expects_json
from flask import request, jsonify, g
from connectors.google.google_connector import GoogleConnector
from models.configuration import Configuration
from repository.datastore.DatastoreRepository import DatastoreRepository as Repository
from repository.scheduler.SchedulerRepository import SchedulerRepository as JobRepository
from services.connector_service import ConnectorService

# Flask and Firebase apps initialization
from services.optimizer_service import OptimizerService

app = Flask(__name__)
firebase_admin.initialize_app()
logging.basicConfig(level=logging.INFO)

# Services to handle requests
global _connector_service


@app.route("/performance")
def performance():
    return {
        'today': random.sample(range(85, 115), 24),
        'yeserday': random.sample(range(75, 120), 24),
        'week': random.sample(range(75, 120), 7),
        'month': random.sample(range(75, 120), 12)
    }


@app.route("/optimizations")
def optimizations():
    logging.info('Calling optimizations to user %s', g.uid)
    return jsonify(_connector_service.get_optimizations(g.uid))


@app.route("/future_optimizations")
def future_optimizations():
    logging.info('Calling future optimizations to user %s', g.uid)
    return jsonify(_connector_service.get_future_optimizations(g.uid))


@app.route("/connectors", methods=['POST'])
@expects_json({
    'type': 'object',
    'properties': {
        'type': {'type': 'string'},
        'configuration': {'type': 'object'}
    },
    'required': ['type', 'configuration']
})
def connectors_post():
    connector_json = request.json

    _connector_service.configure_connector(connector_json['type'], connector_json['configuration'], g.uid)

    return {'status': 'OK'}, 200


@app.route("/connectors")
def connectors():
    return jsonify(_connector_service.get_user_connectors(g.uid))


@app.route("/health")
def health():
    return {'status': 'OK'}, 200


@app.route("/connectors/<connector_type>")
def connector_options(connector_type):
    return jsonify(_connector_service.get_connector_options(connector_type, g.uid))


@app.route("/connectors/<connector_type>", methods=['DELETE'])
def connector_delete(connector_type):
    _connector_service.delete_connector(connector_type, g.uid)

    return {'status': 'OK'}, 200


@app.route("/connectors/<connector_type>/refresh")
def refresh_connector(connector_type):
    _connector_service.refresh_connector(connector_type, g.uid)

    return {'status': 'OK'}, 200


@app.route("/configurations")
def configurations():
    return jsonify(_connector_service.get_configurations(g.uid))


@app.route("/configurations/<configuration_id>", methods=['DELETE'])
def configuration_delete(configuration_id):
    _connector_service.delete_configuration(configuration_id, g.uid)

    return {'status': 'OK'}, 200


@app.route("/configurations", methods=['POST'])
@expects_json({
    'type': 'object',
    'properties': {
        'type': {'type': 'string'},
        'name': {'type': 'string'},
        'ads_account': {'type': 'string'},
        'ads_campaign': {'type': 'string'},
        'adcost_target': {'type': 'number'},
        'ga_account': {'type': 'string'},
        'ga_property': {'type': 'string'},
        'ga_metric': {'type': 'string'},
        'active': {'type': 'boolean'}
    },
    'required': [
        'type',
        'name',
        'ads_account',
        'ads_campaign',
        'adcost_target',
        'ga_account',
        'ga_property',
        'ga_metric',
        'active'
    ]
})
def configurations_post():
    return jsonify(_connector_service.set_configuration(Configuration(**request.json), g.uid))


@app.before_request
def token_id_interceptor():

    # Optimizers (exclude in the future)
    if request.endpoint == 'optimize':
        return

    try:
        g.uid = auth.verify_id_token(request.headers['Authorization'])['uid']
    except Exception:
        return {
                   'status': '401 - Not Authorized'
               }, 401


if __name__ == "__main__":
    # Repository to persist everything
    repository = Repository()

    # Repository to take care of jobs
    job_repository = JobRepository(
        os.environ.get('PROJECT_ID'),
        os.environ.get('LOCATION_ID'),
        os.environ.get('TIMEZONE'),
        os.environ.get('OPTIMIZERS_TOPIC'),
        os.environ.get('OPTIMIZERS_CRON')
    )

    # Google Connector
    google_connector = GoogleConnector(
        os.environ.get('GOOGLE_CLIENT_ID'),
        os.environ.get('GOOGLE_CLIENT_SECRET'),
        os.environ.get('GOOGLE_DEVELOPER_TOKEN'))

    connectors = [google_connector]

    # Connectors modules
    _connector_service = ConnectorService(repository,
                                          job_repository,
                                          connectors)

    _optimization_service = OptimizerService(repository, connectors)

    # Start web server
    app.run()
