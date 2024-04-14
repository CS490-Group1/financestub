from services.financestub_calls import create_request
from services.approved_loans import create_approved_loan_domain, get_approved_loan, loan_approved, monthly_payment, update_loan_domain
from services.transactions import generate_car_transaction, generate_monthly_transaction
from services.financestub_domain import (check_loan_qualify_domain, generate_initial_payment_domain,
                                         validate_payment)

def request_create_domain(info):
    approved = get_approved_loan(info)
    response = check_loan_qualify_domain(info)
    create_request(info, response, approved)
    if response["approved"]:
        return{
            'status':'success',
            'message':'Approve request for loan',
            'code':201
        }
    return{
        'status':'fail',
        'message':'Fail to approve request for loan',
        'code':401
    }

def buy_car_full_domain(info):
    response = validate_payment(info)
    if response["isValid"] == 0:
        return response
    notes = f'''
            Total warranty costs: {info.get("warranties_cost")}
            5% Tax
            '''
    generate_car_transaction(info, response, notes)
    return{
        "status":"success",
        "isValid":1,
        "message":"Successfully created transaction for car",
        'code':200
    }

def buy_car_loan_domain(info):
    response = validate_payment(info)
    if response["isValid"] == 0:
        return response
    create_approved_loan_domain(info)
    notes = f'''
            Down Payment amount: {info.get("down_payment")}
            Total warranty costs: {info.get("warranties_cost")}
            5% Tax
            '''
    generate_car_transaction(info, response, notes)
    response = loan_approved(info, monthly_payment)
    if response['code'] == 500:
        return response
    return{
        "status":"success",
        "isValid":1,
        "message":"Successfully created transaction for car and approved loan",
        'code':200
    }

def pay_loan_domain(info):
    response = validate_payment(info)
    if response["isValid"] == 0:
        return response
    monthly_payment(info)
    notes = f'''Monthly payment: {info.get("amount")}'''
    output = generate_monthly_transaction(info, response, notes)
    if output is None:
        return{
            'status':'fail',
            'message':'Failed to generate monthly transaction',
            "code":500
        }
    return{
        'status':'success',
        'message':'Successfully created monthly transaction',
        "code":201
    }

def incur_interest_domain(info):
    result = update_loan_domain(info)
    if result is None:
        return {
            'status':'fail',
            'message':'Cannot successfully change interest loan',
            'code':500
        }
    return {
        'status':'success',
        'message':'Successfully updated loan to include interest',
        'code':200
    }
