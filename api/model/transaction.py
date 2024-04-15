'''
Test Drive Model

This creates a class that sets predefined attributes relating
to test drive. Later for ORM mapping
'''
# pylint: disable=too-many-arguments, too-few-public-methods, redefined-builtin
class Transaction:
    '''Transaction class'''
    def __init__(self, email, vin, amount, transaction_type,
                 payment_type, company, payment_method):
        self.email = email
        self.vin = vin
        self.amount = amount
        self.transaction_type = transaction_type
        self.payment_type = payment_type
        self.company = company
        self.payment_method = payment_method
