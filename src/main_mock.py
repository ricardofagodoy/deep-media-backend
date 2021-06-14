import random
from firebase_admin import auth
from flask import Flask
from flask_expects_json import expects_json
from flask import request, jsonify, g

# Flask and Firebase apps initialization
app = Flask(__name__)


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
    return jsonify([
        {
            "after": 12,
            "before": 11,
            "campaign": "Test",
            "connector": "",
            "date": "07/06/2021 01:00",
            "id": "1967008233ca4804ace9b0f95f1579e6",
            "margin": 0.005,
            "optimize": "CPA",
            "target": 0.095
        }
    ])


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
    return {
               'status': 'OK'
           }, 200


@app.route("/connectors")
def connectors():
    return jsonify(["google"])


@app.route("/connectors/<connector_type>")
def connector_options(connector_type):
    return {
        "ads_accounts": {
            "3013036305": [],
            "4413234797": [
                "Website traffic-Search-1"
            ]
        },
        "ga_accounts": {
            "111207543": {
                "name": "ricardofagodoy.github.io",
                "properties": {
                    "UA-111207543-1": [
                        {
                            "index": 1,
                            "name": "conversion"
                        },
                        {
                            "index": 2,
                            "name": "conv"
                        }
                    ]
                }
            },
            "187669733": {
                "name": "Melhor C\u00f3digo",
                "properties": {}
            },
            "188017198": {
                "name": "Aporte F\u00e1cil",
                "properties": {}
            },
            "76876633": {
                "name": "AdMob pub-2813072672105928",
                "properties": {
                    "UA-76876633-1": [],
                    "UA-76876633-2": [],
                    "UA-76876633-3": [],
                    "UA-76876633-4": [],
                    "UA-76876633-5": [],
                    "UA-76876633-6": []
                }
            }
        }
    }


@app.route("/configurations")
def configurations():
    return jsonify([
        {
            "active": False,
            "adcost_target": 9.6,
            "name": "Minha Config 01",
            "ads_account": "4413234797",
            "ads_campaign": "Website traffic-Search-1",
            "ga_account": "111207543",
            "ga_metric": "1",
            "ga_property": "UA-111207543-1",
            "id": "936442ee09644d72949b24fb56b34a47",
            "type": "google"
        },
        {
            "active": True,
            "adcost_target": 9.6,
            "name": "Minha Config 02",
            "ads_account": "4413234797",
            "ads_campaign": "Website traffic-Search-1",
            "ga_account": "111207543",
            "ga_metric": "1",
            "ga_property": "UA-111207543-1",
            "id": "936442ee096446b34a47",
            "type": "google"
        }
    ])


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
    config = request.json

    if not config.get('id'):
        config['id'] = random.randint(1, 1000000)

    return config


if __name__ == "__main__":
    app.run()
