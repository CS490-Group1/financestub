from services.financestub_domain import (
    check_loan_qualify_domain, generate_apr_credit_score_domain,
    generate_initial_payment_domain, generate_required_payment_domain,
    validate_bank_payment_domain, validate_card_payment_domain)

def generate_initial_payment_app(info):
    return generate_initial_payment_domain(info)

def check_loan_qualify_app(info):
    return check_loan_qualify_domain(info)

def generate_apr_credit_score_app():
    return generate_apr_credit_score_domain()

def generate_required_payment_app(info):
    return generate_required_payment_domain(info)

def validate_card_payment_app(info):
    return validate_card_payment_domain(info)

def validate_bank_payment_app(info):
    return validate_bank_payment_domain(info)
