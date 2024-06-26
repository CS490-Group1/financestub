'''
Finance payment App

This directs traffic relating to the finance payment
app from the endpoints
'''
# pylint: disable=import-error
from services.request_loans import clear_user_requests_domain
from services.transactions import (delete_all_transactions_domain,
                                   get_all_transactions_domain, 
                                   get_monthly_sales_report_domain,
                                   get_transaction_type_domain)
from services.finance_payments import (buy_car_full_domain,
                                    buy_car_loan_domain, incur_interest_domain,
                                    pay_loan_domain, request_create_domain,
                                    buy_services_domain)

def buy_car_full_app(info):
    '''buy car with full payment based on passed in info'''
    return buy_car_full_domain(info)

def buy_car_loan_app(info):
    '''buy car with loan based on passed in info'''
    return buy_car_loan_domain(info)

def buy_services_app(info):
    '''buy services based on passed in info'''
    return buy_services_domain(info)

def pay_loan_app(info):
    '''pay loan based on info'''
    return pay_loan_domain(info)

def request_create_app(info):
    '''create request based on info'''
    return request_create_domain(info)

def incur_interest_app(info):
    '''incur interest once month past'''
    return incur_interest_domain(info)

def clear_user_transactions_app(info):
    '''clear user transactions'''
    return delete_all_transactions_domain(info)

def clear_user_requests_app(info):
    '''clear user requests'''
    return clear_user_requests_domain(info)

def get_user_transactions_app(info):
    '''get transaction history of user'''
    return get_all_transactions_domain(info)

def get_transaction_type_app(info):
    '''get transaction type based on info'''
    return get_transaction_type_domain(info)

def get_monthly_sales_report_app(info):
    '''get all transaction history of given month and year'''
    return get_monthly_sales_report_domain(info)
