'''
Loans Domain

Layer where loan functions resides
'''
# pylint: disable=import-error, no-name-in-module
from decimal import Decimal
from api.model.approved_loan import Approved_Loan
from data.approved_loan_storage import (grab_approved_loan, delete_approved_loan,
                               store_approved_loan, pay_monthly_loan, update_loan)
from services.request_loans import get_recent_request_domain, reject_pending_domain, update_request_domain
from services.financestub_domain import (generate_initial_payment_domain,
                                        generate_required_payment_domain)

def create_approved_loan_domain(info):
    '''
    create customer apr if customer
    has not have their apr logged
    '''
    request = get_recent_request_domain(info)
    if request:
        reject_pending_domain(request.request_id)
    initial = generate_initial_payment_domain(request.actual_loan_amount)
    new_approved = Approved_Loan(request.request_id, request.email,
                                 request.vin, request.apr, initial["loan_amount"],
                                 initial["loan_amount"], initial["monthly_payment"])
    new_approval_id = store_approved_loan(new_approved)
    return new_approval_id

def approval_to_json(approval):
    '''convert approval to json'''
    return{
        "request_id":approval.request_id,
        "email":approval.email,
        "vin":approval.vin,
        "apr":approval.apr,
        "initial_loan_amount":approval.initial_loan_amount,
        "current_loan_amount":approval.current_loan_amount,
        "monthly_payment":approval.monthly_payment,
        "created":approval.created,
        "last_updated":approval.last_updated
    }

def get_approved_loan(info):
    '''get approved loan associated with the user id'''
    response = grab_approved_loan(info)
    if not response:
        return None
    return approval_to_json(response)

def monthly_payment(info):
    '''pay monthly loan, update approval loan based on amount passed in'''
    response = get_approved_loan(info)
    total = Decimal(response['current_loan_amount']) - Decimal(info.get("amount"))
    pay_monthly_loan(total, response)
    if not total:
        update_request_domain(info, "paid")
        delete_approved_loan(info)

def update_loan_domain(info):
    '''update approval loan for incurred interest'''
    response = get_approved_loan(info)
    output = generate_required_payment_domain(response)
    return update_loan(output, info.get("email"))
