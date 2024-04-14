from services.payments import (buy_car_full_domain, buy_car_loan_domain,
                               pay_loan_domain,
                               )

def buy_car_full_app(info):
    '''buy car with full payment based on passed in info'''
    return buy_car_full_domain(info)

def buy_car_loan_app(info):
    '''buy car with loan based on passed in info'''
    return buy_car_loan_domain(info)

def pay_loan_app(info):
    '''pay loan based on info'''
    return pay_loan_domain(info)
