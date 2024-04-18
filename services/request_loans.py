'''
Request Loan Domain

Layer where request functions resides
'''
# pylint: disable=import-error
from data.request_loan_storage import (clear_user_requests, get_last_request, get_recent_request,
                                       create_request, reject_pending, update_request)
from api.model.request_loan import Request_Loan
from services.financestub_domain import generate_apr_credit_score_domain

def create_request_domain(info, response, approved, notes):
    '''create request based on info'''
    request = get_last_request(info)
    if not request:
        output = generate_apr_credit_score_domain()
    else:
        output = {
            "credit_score":request.credit_score,
            "apr":request.apr
        }
    new_request = Request_Loan(info.get("email"), output["credit_score"], output["apr"],
                                info.get("vin"), info.get("income"), info.get("total"),
                                info.get("down_payment"), response.get("max_loan_amount"),
                                response.get("actual_loan_amount"), approved)
    create_request(new_request, notes)

def get_recent_request_domain(info):
    '''get recent approved request'''
    return get_recent_request(info)

def reject_pending_domain(request_id):
    '''reject pending approved request'''
    reject_pending(request_id)

def update_request_domain(info, status):
    '''update request with status'''
    request_id = get_recent_request_domain(info).request_id
    update_request(status, request_id)

def get_finance_report_domain(info):
    '''get finance report of user'''
    request = get_last_request(info)
    if not request:
        return None
    return {
        "email":request.email,
        "apr":request.apr,
        "credit_score":request.credit_score,
        "income":request.income,
        "vin":request.vin,
        "car_price":request.car_price,
        "down_payment":request.down_payment,
        "max_loan_amount":request.max_loan_amount,
        "actual_loan_amount":request.actual_loan_amount,
        "approved":request.approved
    }

def clear_user_requests_domain(info):
    '''clear user requests'''
    return clear_user_requests(info)
