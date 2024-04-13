'''
Test Drive Model

This creates a class that sets predefined attributes relating
to test drive. Later for ORM mapping
'''
# pylint: disable=too-many-arguments, too-few-public-methods, redefined-builtin
class Transaction:
    '''Transaction class'''
    def __init__(self, user_id, amount, type, company, payment_method):
        self.user_id = user_id
        self.amount = amount
        self.type = type
        self.company = company
        self.payment_method = payment_method
