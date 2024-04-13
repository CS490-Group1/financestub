'''
Loan Model

This creates a class that sets predefined attributes relating to loan. Later for ORM mapping
'''
# pylint: disable=too-many-instance-attributes, too-many-arguments, too-few-public-methods
class Loan:
    '''Loan class'''
    def __init__(self, email, vin, credit_score, apr,
                  approved_loan=0, loan_amount=0, monthly_payment=0, approved=0):
        self.email = email
        self.vin = vin
        self.credit_score = credit_score
        self.apr = apr
        self.approved_loan = approved_loan
        self.loan_amount = loan_amount
        self.monthly_payment = monthly_payment
        self.approved = approved
