import sys
import os
from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(parent_dir)

# pylint: disable=wrong-import-position
from payment_app import buy_car_full_app, buy_car_loan_app, incur_interest_app, pay_loan_app, request_create_app

app = Flask(__name__)

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/documentation.yaml'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

app.register_blueprint(swaggerui_blueprint)

## This is going to be a simple financal stub for the online car dealership ##
# @app.post("get/user/transactions")
# def handle_get_user_transactions():
#     '''handle get user transactions'''
#     info = request.json
#     response = get_user_transactions_app(info)
#     return jsonify(response), 200

@app.post("/buy/car/full")
def handle_buy_car_full():
    '''handles buying car at full price'''
    info = request.json
    response = buy_car_full_app(info)
    return jsonify(response), response["code"]

@app.post("/buy/car/loan")
def handle_buy_car_full():
    '''handles buying car at a down payment'''
    info = request.json
    response = buy_car_loan_app(info)
    return jsonify(response), response["code"]

@app.patch("/pay/loan")
def handle_pay_loan():
    '''pay loan based on amount'''
    info=response.json
    response = pay_loan_app(info)
    return jsonify(response), response["code"]

@app.post("/create/request")
def handle_request_creation():
    '''
    Create request and determine if accept or deny based
    on info
    '''
    info = request.json
    response = request_create_app(info)
    return jsonify(response), response["code"]

@app.patch("/incur/interest")
def handle_incur_interest():
    '''incur interest when month passes'''
    info=request.json
    response = incur_interest_app(info)
    return jsonify(response), 200

if __name__ == "__main__":
    app.run(debug=True, port=8001)
