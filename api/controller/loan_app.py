from services.loans import (create_approval_domain, delete_approved_loan_domain,
                            get_approved_loan, update_approval_domain,
                            )

def create_approval_app(info):
    return create_approval_domain(info)

def get_approved_loan_app(info):
    return get_approved_loan(info)

def update_approval_loan_app(info):
    return update_approval_domain(info)

def delete_approved_loan_app(info):
    delete_approved_loan_domain(info)
