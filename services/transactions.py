'''
Transactions Domain

Layer where transactions functions resides
'''
# pylint: disable=import-error, no-name-in-module
from api.model.transaction import Transaction
from data.transaction_storage import (store_car_transaction,
                    store_monthly_transaction, get_transactions,
                    delete_all_transactions)

def generate_car_transaction(info, response, notes):
    '''generate car transactions based on passed in info'''
    
    new_transaction = Transaction(info.get("email"), info.get("vin"), info.get("total"),
                                info.get("transaction_type"), info.get("payment_type"),
                                info.get("company"), response["payment_method"])
    store_car_transaction(new_transaction, info, notes)

def generate_monthly_transaction(info, response, notes):
    '''generate monthly transaction based on passed in info'''
    new_transaction = Transaction(info.get("email"), info.get("vin"), info.get("amount"),
                                1, info.get("payment_type"), info.get("company"),
                                response["payment_method"])
    monthly_transaction_id = store_monthly_transaction(new_transaction, notes)
    return monthly_transaction_id

def get_all_transactions_domain(user_id):
    '''get all transactions based on user id'''
    transactions = []
    transactions_table = get_transactions(user_id)
    for transaction in transactions_table:
        transaction_json = {
            "transaction_id":transaction.transaction_id,
            "amount": transaction.amount,
            "type": transaction.type,
            "company": transaction.company,
        }
        transactions.append(transaction_json)
    return transactions

def delete_all_transactions_domain(transaction_id):
    '''delete transaction and all sub transactions based on transaction id'''
    delete_all_transactions(transaction_id)
