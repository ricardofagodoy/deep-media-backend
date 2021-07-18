import os
import logging
from time import strftime
import firebase_admin
from datetime import datetime
from firebase_admin import auth
from flask import Flask
from flask_expects_json import expects_json
from flask import request, jsonify, g
from pytz import timezone
from connectors.google.google_connector import GoogleConnector
from models.configuration import Configuration
from repository.datastore.DatastoreRepository import DatastoreRepository as Repository
from repository.scheduler.SchedulerRepository import SchedulerRepository as JobRepository
from services.MessageException import MessageException
from services.connector_service import ConnectorService

# Flask and Firebase apps initialization
app = Flask(__name__)
firebase_admin.initialize_app()

logging.basicConfig(level=logging.INFO)

# Repository to persist everything
repository = Repository()

TIMEZONE = timezone(os.environ.get('TIMEZONE'))

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


@app.route("/health")
def health():
    return {'status': 'OK'}, 200


@app.route("/performance/<configuration_id>")
def performance(configuration_id):

    # Expected date format for this API
    date_format = '%d/%m/%Y'

    # Filters to pull performance ticks
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if start_date:
        start_date = TIMEZONE.localize(datetime.strptime(start_date, date_format))

    if end_date:
        end_date = TIMEZONE.localize(datetime.strptime(end_date, date_format))

    return jsonify(_connector_service.get_performance(configuration_id, g.uid, start_date, end_date))


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
        'ga_profile': {'type': 'string'},
        'ga_dimension': {'type': 'string'},
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
        'ga_profile',
        'ga_dimension',
        'ga_metric',
        'active'
    ]
})
def configurations_post():
    return jsonify(_connector_service.set_configuration(Configuration(**request.json), g.uid))


@app.before_request
def token_id_interceptor():
    if request.method in ['POST', 'GET', 'DELETE', 'PATCH', 'PUT']:
        try:
            g.uid = auth.verify_id_token(request.headers['Authorization'])['uid']
        except Exception:
            return {'status': '401 - Not Authorized'}, 401


@app.after_request
def after_request(response):

    timestamp = strftime('[%d/%m/%Y %H:%M]')
    logging.info('%s %s %s %s %s %s', timestamp,
                 request.remote_addr,
                 request.method,
                 request.scheme,
                 request.full_path,
                 response.status)

    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')

    return response


@app.errorhandler(MessageException)
def message_exception_handler(error: MessageException):
    logging.error(error, exc_info=True)
    return {'error': str(error)}, 500


@app.errorhandler(Exception)
def all_exception_handler(error: Exception):
    logging.error(error, exc_info=True)
    return {'error': 'Internal Error'}, 500


if __name__ == "__main__":
    app.run()
