import sys
import os
from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(parent_dir)

# pylint: disable=wrong-import-position
# from finance_payment_app import (buy_car_full_app, buy_car_loan_app, buy_services_app,
#                          clear_user_requests_app, clear_user_transactions_app,
#                          incur_interest_app, pay_loan_app, request_create_app,
#                          get_user_transactions_app, get_monthly_sales_report_app)
# from loan_app import get_finance_report_app, get_user_approved_loan_app

app = Flask(__name__)
CORS(app)

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = 'https://raw.githubusercontent.com/CS490-Group1/financestub/dev/static/documentation.yaml'  # Our API url

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
@app.post("/get/user/transactions")
def handle_get_user_transactions():
    '''handle get user transactions'''
    info = request.json
    response = get_user_transactions_app(info)
    return jsonify(response), 200

@app.post("/buy/car/full")
def handle_buy_car_full():
    '''handles buying car at full price'''
    info = request.json
    response = buy_car_full_app(info)
    return jsonify(response), response["code"]

@app.post("/buy/car/loan")
def handle_buy_car_loan():
    '''handles buying car at a down payment'''
    info = request.json
    response = buy_car_loan_app(info)
    return jsonify(response), response["code"]

@app.post("/buy/services")
def handle_buy_services():
    '''handles buying services'''
    info = request.json
    response = buy_services_app(info)
    return jsonify(response), response["code"]

@app.patch("/pay/loan")
def handle_pay_loan():
    '''pay loan based on amount'''
    info=request.json
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

@app.post("/get/approved/loan")
def handle_get_user_approved_loan():
    '''get approved loan related to user'''
    info = request.json
    response = get_user_approved_loan_app(info)
    return jsonify(response), 200

@app.post("/get/finance/report")
def handle_get_finance_report():
    '''get finance report related to user'''
    info = request.json
    response = get_finance_report_app(info)
    return jsonify(response), 200

@app.post("/clean/user/transactions")
def handle_clear_user_transactions():
    '''clear user transactions'''
    info=request.json
    clear_user_transactions_app(info)
    return jsonify({"status":"success"})

@app.post("/clean/user/requests")
def handle_clear_user_requests():
    '''clear user requests'''
    info=request.json
    clear_user_requests_app(info)
    return jsonify({"status":"success"})

@app.post("/get/monthly_sales_report")
def handle_get_monthly_sales_report(info):
    '''retrieves all sales information for given month and year'''
    info=request.json
    response = get_monthly_sales_report_app(info)

if __name__ == "__main__":
    app.run(debug=True, port=8001)
