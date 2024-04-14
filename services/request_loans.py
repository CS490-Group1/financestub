from data.request_loan_storage import get_recent_request, create_request
from api.model.request_loan import Request_Loan
from services.financestub_domain import generate_apr_credit_score_domain

def create_request_domain(info, response, approved):
    output = approved["request_id"]
    if not output:
        output = generate_apr_credit_score_domain()
    new_request = Request_Loan(info.get("email"), info.get("credit_score"), output.get("apr"),
                                info.get("vin"), info.get("income"), info.get("car_price"),
                                info.get("down_payment"), response.get("max_loan_amount"),
                                info.get("actual_loan_amount"), response.get("approved"))
    create_request(new_request)

def get_recent_request_domain(info):
    return get_recent_request(info)
