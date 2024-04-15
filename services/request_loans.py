from data.request_loan_storage import get_last_request, get_recent_request, create_request, reject_pending, update_request
from api.model.request_loan import Request_Loan
from services.financestub_domain import generate_apr_credit_score_domain

def create_request_domain(info, response, approved):
    request = get_last_request(info)
    if not request:
        output = generate_apr_credit_score_domain()
    else:
        output = {
            "credit_score":request.credit_score,
            "apr":request.apr
        }
    new_request = Request_Loan(info.get("email"), output["credit_score"], output["apr"],
                                info.get("vin"), info.get("income"), info.get("car_price"),
                                info.get("down_payment"), response.get("max_loan_amount"),
                                response.get("actual_loan_amount"), approved)
    create_request(new_request)

def get_recent_request_domain(info):
    return get_recent_request(info)

def reject_pending_domain(request_id):
    reject_pending(request_id)

def update_request_domain(info, status):
    request_id = get_recent_request_domain(info).request_id
    update_request(status, request_id)
    