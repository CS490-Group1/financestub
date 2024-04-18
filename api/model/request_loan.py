'''
Request Loan Model

This creates a class that sets predefined attributes relating to requested loans.
Later for ORM mapping
'''
# pylint: disable=too-many-instance-attributes, too-many-arguments, too-few-public-methods
class Request_Loan:
    '''Loan class'''
    def __init__(self, email, credit_score, apr, vin,
                  income=0, total=0, down_payment=0,
                  max_loan_amount=0, actual_loan_amount=0,
                  approved=0):
        self.email = email
        self.credit_score = credit_score
        self.apr = apr
        self.vin = vin
        self.income = income
        self.total = total
        self.down_payment = down_payment
        self.max_loan_amount = max_loan_amount
        self.actual_loan_amount = actual_loan_amount
        self.approved = approved
