'''
Loans Domain

Layer where loan functions resides
'''
# pylint: disable=import-error, no-name-in-module
from decimal import Decimal
from api.model.loan import Loan
from data.loan_storage import (grab_approved_loan, delete_approved_loan,
                               store_new_loan, update_approval,
                               down_payment, pay_monthly_loan, update_loan)
from services.financestub_domain import (generate_apr_credit_score_domain,
                                        generate_required_payment_domain)

def create_approval_domain(info):
    '''
    create customer apr if customer
    has not have their apr logged
    '''
    response = generate_apr_credit_score_domain()
    apr = response["apr"]
    credit_score = response["credit_score"]
    new_loan = Loan(info.get("email"), credit_score, apr)
    new_approval_id = store_new_loan(new_loan)
    return new_approval_id

def approval_to_json(approval, email):
    '''convert approval to json'''
    return{
        "email":email,
        "apr":approval.apr,
        "credit_score":approval.credit_score,
        "loan_amount":approval.loan_amount,
        "monthly_payment":approval.monthly_payment,
        "approved":approval.approved,
        "created":approval.created,
        "last_updated":approval.last_updated
    }

def get_approved_loan(info):
    '''get approved loan associated with the user id'''
    response, email = grab_approved_loan(info)
    if not response:
        return None
    return approval_to_json(response, email)

def delete_approved_loan_domain(info):
    '''delete approved loan based on user id'''
    response = get_approved_loan(info)
    if not response:
        return None
    if response["loan_amount"] > 0:
        return {
            'status': 'fail',
            'message': 'Unable to delete approval',
            'code': 500
        }
    delete_approved_loan(info)
    return {
        'status': 'success',
        'message': 'Successfully deleted approval',
        'code': 200
    }

def update_approval_domain(info):
    '''update approval loan based on approved and user id'''
    return update_approval(info)

def loan_approved(info, monthly_payment_info):
    '''modify approval loan to update loan amount and monthly payment'''
    response = down_payment(info, monthly_payment_info)
    if response == 'error':
        return {
            'status': 'fail',
            'message': 'Unable to store down payment',
            'code': 500
        }
    return {
        'status': 'success',
        'message': 'Successfully approved loan',
        'code': 200
    }

def monthly_payment(info):
    '''pay monthly loan, update approval loan based on amount passed in'''
    response = get_approved_loan(info)
    total = Decimal(response['loan_amount']) - Decimal(info.get("amount"))
    pay_monthly_loan(total, response)

def update_loan_domain(info):
    '''update approval loan for incurred interest'''
    output = generate_required_payment_domain(info)
    return update_loan(output, info.get("email"))
    