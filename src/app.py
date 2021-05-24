import random
from flask_expects_json import expects_json
from flask import request, make_response, jsonify
from repository.DatastoreRepository import DatastoreRepository as Repository
from flask import Flask

app = Flask(__name__)
_repository = Repository()

# Schemas
schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'email': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': ['email', 'password']
}


@app.route("/optimizations")
def optimizations():
    return jsonify([{
        'date': '22/05/2021 18:00',
        'campaign': 'Campanha 01',
        'target': 0.1,
        'margin': 0.05,
        'optimize': 'CPA',
        'before': 12.50,
        'after': 14
    }] * 20)


@app.route("/performance")
def performance():
    return {
        'today': random.sample(range(50, 200), 24),
        'yeserday': random.sample(range(50, 200), 24),
        'week': random.sample(range(50, 200), 7),
        'month': random.sample(range(50, 200), 12)
    }


@app.route("/connectors", methods=['GET', 'POST'])
def connectors():

    if request.method == 'GET':
        return jsonify([
            'google'
        ])

    if request.method == 'POST':
        print(request.json)
        return 'OK', 200


@app.route("/connectors/<connector>")
def connector_options(connector):
    return {
        'ads_accounts': {
            'Ads Account 1': ['Campaign 01', 'Campaign 02']
        },
        'ga_accounts': {
            'GA Account 1': {
                'Property 1': ['metric1', 'metric2']
            }
        }
    }


@app.route("/configurations", methods=['GET', 'POST'])
def configurations():

    if request.method == 'GET':
        return jsonify([])

    if request.method == 'POST':
        print(request.json)
        return jsonify([request.json])


if __name__ == "__main__":
    app.run(host='0.0.0.0')
