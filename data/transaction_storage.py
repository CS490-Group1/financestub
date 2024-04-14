'''
Transactions Data

Layer where all transaction related functions talk to the database
'''
# pylint: disable=import-error
from datetime import datetime
from sqlalchemy.orm import Session
from data.alchemy_setup import engine
from data.alchemy_classes import (
    Transactions, Transactions_Cars,
    Transactions_Warranties, Transactions_Services)

def store_car_transaction(new_transaction, info, notes):
    '''store car transaction based on passed in params'''
    created_id = 0
    time = datetime.now()
    transaction = Transactions(
        email=new_transaction.email,
        vin=new_transaction.vin,
        amount=new_transaction.amount,
        transaction_type=new_transaction.transaction_type,
        payment_type=new_transaction.payment_type,
        company=new_transaction.company,
        payment_method=new_transaction.payment_method,
        created=time,
        last_updated=time, notes=notes
    )

    transaction_warranties = []
    for warranty in info.get("warranties"):
        transaction_warranty = Transactions_Warranties(
            warranty_name = warranty,
            created=time,
            last_updated=time, notes=''
        )
        transaction_warranty.transactions = transaction
        transaction_warranties.append(transaction_warranty)

    with Session(engine) as session:
        session.add(transaction)
        for transaction_warranty in transaction_warranties:
            session.add(transaction_warranty)
        session.commit()
        created_id = transaction.transaction_id
    return created_id

def store_monthly_transaction(new_transaction, notes):
    '''store monthly transaction based on passed in info'''
    created_id = 0
    time = datetime.now()
    transaction = Transactions(
        user_id=new_transaction.user_id,
        amount=new_transaction.amount,
        type=new_transaction.type,
        company=new_transaction.company,
        payment_method=new_transaction.payment_method,
        created=time,
        last_updated=time, notes=notes
    )

    with Session(engine) as session:
        session.add(transaction)
        session.commit()
        created_id = transaction.transaction_id
    return created_id

def get_transactions(email):
    '''get transactions based on user id'''
    with Session(engine) as session:
        result = session.query(
            Transactions
        ).filter(
            Transactions.email == email,
        ).all()
    return result

def get_car_transactions(email):
    '''get car transactions based on user id'''
    with Session(engine) as session:
        result = session.query(
            Transactions, Transactions_Cars.vin
        ).join(
            Transactions_Cars
        ).filter(
            Transactions.email == email
        ).all()
    return result

def delete_all_transactions(transaction_id):
    '''delete all transactions and sub transactions based on transaction id'''
    with Session(engine) as session:
        car_transaction = session.query(
            Transactions_Cars
        ).filter(
            Transactions_Cars.transaction_id == transaction_id
        ).first()
        if car_transaction:
            session.delete(car_transaction)

        service_transactions = session.query(
            Transactions_Services
        ).filter(
            Transactions_Services.transaction_id == transaction_id
        ).all()
        if service_transactions:
            for service_transaction in service_transactions:
                session.delete(service_transaction)

        warranty_transactions = session.query(
            Transactions_Warranties
        ).filter(
            Transactions_Warranties.transaction_id == transaction_id
        ).all()
        if warranty_transactions:
            for warranty_transaction in warranty_transactions:
                session.delete(warranty_transaction)

        transaction = session.query(
            Transactions
        ).filter(
            Transactions.transaction_id == transaction_id
        ).first()
        if transaction:
            session.delete(transaction)
        session.commit()
