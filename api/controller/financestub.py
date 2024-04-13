import sys
import os
from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(parent_dir)

# pylint: disable=wrong-import-position
from loan_app import (create_approval_app, get_approved_loan_app,
                    delete_approved_loan_app, update_approval_loan_app)
from financestub_app import (check_loan_qualify_app, generate_apr_credit_score_app,
    generate_initial_payment_app, generate_required_payment_app, validate_bank_payment_app,
    validate_card_payment_app)

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

@app.get("/creditcheck")
def creditCheck():
    '''generate apr from random credit score'''
    response = generate_apr_credit_score_app()
    return jsonify(response), 200

@app.post("/loanqualification")
def loanQualification():
    info = request.json
    response = check_loan_qualify_app(info)
    return jsonify(response), 200

@app.post("/initialpayment")
def generateInitialPayment():
    info = request.json
    response = generate_initial_payment_app(info)
    return jsonify(response), 200

@app.post("/payment")
def generatePayment():
    info = request.json
    response = generate_required_payment_app(info)
    return jsonify(response), 200

@app.post("/validatebankpayment")
def validateBankPayment():
    info = request.json
    response = validate_bank_payment_app(info)
    return jsonify(response), response["code"]

@app.post("/validatecardpayment")
def validateCardPayment():
    info = request.json
    response = validate_card_payment_app(info)
    return jsonify(response), response["code"]

@app.post("/get/user/approval")
def get_profile_approval():
    info = request.json
    response = get_approved_loan_app(info)
    return jsonify(response), 200

@app.post("/create/approval")
def handle_create_approval():
    info = request.json
    response = create_approval_app(info)
    return jsonify(response), response["code"]

@app.patch("/update/approval")
def handle_update_approval():
    info = request.json
    response = update_approval_loan_app(info)
    return jsonify(response), response["code"]

@app.post("/delete/user/approval")
def delete_profile_approval():
    info = request.json
    response = delete_approved_loan_app(info)
    return jsonify(response), response["code"]

if __name__ == "__main__":
    app.run(debug=True, port=8001)
