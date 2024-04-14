'''
Approved Loan Model

This creates a class that sets predefined attributes relating to approved loan.
Later for ORM mapping
'''
# pylint: disable=too-many-instance-attributes, too-many-arguments, too-few-public-methods
class Approved_Loan:
    '''Loan class'''
    def __init__(self, request_id, email, vin, apr, initial_loan_amount=0,
                current_loan_amount=0, monthly_payment=0):
        self.request_id = request_id
        self.email = email
        self.vin = vin
        self.apr = apr
        self.initial_loan_amount = initial_loan_amount
        self.current_loan_amount = current_loan_amount
        self.monthly_payment = monthly_payment
