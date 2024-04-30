'''
Loan App

This directs traffic relating to the loan
app from the endpoints
'''
# pylint: disable=import-error
from services.request_loans import get_finance_report_domain
from services.approved_loans import get_approved_loan

def get_user_approved_loan_app(info):
    '''delete all info relating to user'''
    return get_approved_loan(info)

def get_finance_report_app(info):
    '''get finance report of user'''
    return get_finance_report_domain(info)
