import os
import random
import firebase_admin
from firebase_admin import auth
from flask import Flask
from flask_expects_json import expects_json
from flask import request, jsonify, g
from connectors.google.google_ads_connector import GoogleAdsConnector
from repository.DatastoreRepository import DatastoreRepository as Repository
from services.connector_service import ConnectorService

# Flask and Firebase apps initialization
app = Flask(__name__)
firebase_admin.initialize_app()

# Services to handle requests
global _connector_service


@app.route("/optimizations")
def optimizations():
    return {
        'history': [{
            'date': '27/05/2021 18:00',
            'campaign': 'Campanha 01',
            'target': 0.1,
            'margin': 0.05,
            'optimize': 'CPA',
            'before': 12.50,
            'after': 14
        }] * 20,
        'future': '28/05/2021 11:00'
    }


@app.route("/performance")
def performance():
    return {
        'today': random.sample(range(50, 200), 24),
        'yeserday': random.sample(range(50, 200), 24),
        'week': random.sample(range(50, 200), 7),
        'month': random.sample(range(50, 200), 12)
    }


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

    return {
        'status': 'OK'
    }, 200


@app.route("/connectors")
def connectors():
    return jsonify(_connector_service.get_user_connectors(g.uid))


@app.route("/connectors/<connector_type>")
def connector_options(connector_type):
    return _connector_service.get_connector_options(connector_type, g.uid)


@app.route("/configurations")
def configurations():
    return jsonify([])


@app.route("/configurations", methods=['POST'])
@expects_json({
    'type': 'object',
    'properties': {
        'type': {'type': 'string'},
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
    print(request.json)
    return jsonify([request.json])


@app.before_request
def token_id_interceptor():

    try:
        g.uid = auth.verify_id_token(request.headers['Authorization'])['uid']
    except Exception:
        return {
            'status': '401 - Not Authorized'
        }, 401


if __name__ == "__main__":

    # Repository to persist everything
    repository = Repository()

    # Google Connector
    google_connector = GoogleAdsConnector(
        os.environ.get('GOOGLE_CLIENT_ID'),
        os.environ.get('GOOGLE_CLIENT_SECRET'),
        os.environ.get('GOOGLE_DEVELOPER_TOKEN'))

    # Connectors modules
    _connector_service = ConnectorService(repository, [
        google_connector
    ])

    # Start web server
    app.run()
