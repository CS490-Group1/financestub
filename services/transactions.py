'''
Transactions Domain

Layer where transactions functions resides
'''
# pylint: disable=import-error, no-name-in-module
from api.model.transaction import Transaction
from data.transaction_storage import (store_car_transaction,
                    store_monthly_transaction, get_transactions,
                    delete_all_transactions, store_service_transaction)

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

def generate_services_transaction(info, response, notes):
    '''generate service transactions based on passed in info'''
    new_transaction = Transaction(info.get("email"), info.get("vin"), info.get("total"),
                                info.get("transaction_type"), info.get("payment_type"),
                                info.get("company"), response["payment_method"])
    store_service_transaction(new_transaction, info, notes)

# def get_all_transactions_domain(info):
#     '''get all transactions based on user id'''
#     transactions = []
#     transactions_table = get_transactions(info)
#     for transaction in transactions_table:
#         transaction_json = {
#             "transaction_id":transaction.transaction_id,
#             "amount": transaction.amount,
#             "transaction_type": transaction.transaction_type,
#             "company": transaction.company,
#             "notes":transaction.notes
#         }
#         if transaction.transaction_type == 3:
#             response = get_services_transactions(
#             transaction.transaction_id)
#         else:
#             response = get_warranties_transactions(
#             transaction.transaction_id)
#             if response:
#                 warranties = []
#                 for warranty in response.warranty_name:
#                     warranties = 
        
#         transactions.append(transaction_json)
#     return transactions

def delete_all_transactions_domain(info):
    '''delete transaction and all sub transactions based on transaction id'''
    transactions_table = get_transactions(info)
    for transaction in transactions_table:
        delete_all_transactions(transaction.transaction_id)
