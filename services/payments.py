'''
Payment Domain

Layer where payment functions resides
'''
# pylint: disable=import-error
from services.request_loans import create_request_domain
from services.approved_loans import (create_approved_loan_domain, get_approved_loan,
                                    monthly_payment, update_loan_domain)
from services.transactions import (generate_car_transaction,
                                    generate_services_transaction,
                                    generate_monthly_transaction)
from services.financestub_domain import (check_loan_qualify_domain,
                                         validate_payment)

def request_create_domain(info):
    '''create request with info'''
    approved_loan = get_approved_loan(info)
    response = check_loan_qualify_domain(info)
    approved = response["approved"]
    notes = ""
    if not approved:
        notes = "Does not qualify loan"
    if approved_loan:
        approved = 0
        notes = "Already has loan active"
    create_request_domain(info, response, approved, notes)
    if response["approved"]:
        return{
            'status':'success',
            'message':'Approve request for loan',
            "approved":response["approved"],
            'code':201
        }
    return{
        'status':'fail',
        'message':'Fail to approve request for loan',
        "approved":response["approved"],
        'code':401
    }

def buy_car_full_domain(info):
    '''buy car with full payment'''
    response = validate_payment(info)
    if response["isValid"] == 0:
        return response
    notes = f'''
            Car Price: {info.get("car_price")}
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
    '''buy car with loan'''
    result = get_approved_loan(info)
    if result:
        return{
            "status":"fail",
            "message":'''Something did not go as planned.
            Cannot create an approved loan when there is an
            existing loan.''',
            "code":500
        }
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
    return{
        "status":"success",
        "isValid":1,
        "message":"Successfully created transaction for car and approved loan",
        'code':200
    }

def buy_services_domain(info):
    '''buy services'''
    response = validate_payment(info)
    if response["isValid"] == 0:
        return response
    notes = f'''
            Total service costs: {info.get("services_cost")}
            Total warranty discount: {info.get("warranties_discount")}
            5% Tax
            '''
    generate_services_transaction(info, response, notes)
    return{
        "status":"success",
        "isValid":1,
        "message":"Successfully created transaction for services",
        'code':200
    }

def pay_loan_domain(info):
    '''pay loan'''
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
    '''incur interest'''
    result = update_loan_domain(info)
    if not result:
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
