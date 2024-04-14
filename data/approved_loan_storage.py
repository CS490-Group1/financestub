'''
Loan Data

Layer where all loan related functions talk to the database
'''
# pylint: disable=import-error
from datetime import datetime
from sqlalchemy.orm import Session
from data.alchemy_setup import engine
from data.alchemy_classes import Approved_Loans

def grab_approved_loan(info):
    '''grab approved loan based on user id'''
    with Session(engine) as session:
        result = session.query(Approved_Loans
        ).filter(
            Approved_Loans.email == info.get("email")
        ).first()
    return result

def store_approved_loan(new_approved):
    '''store new loan based on passed in info'''
    created_id = 0
    time = datetime.now()
    approval = Approved_Loans(
        request_id=new_approved.request_id,
        email=new_approved.email,
        vin=new_approved.vin,
        apr=new_approved.apr,
        initial_loan_amount=new_approved.initial_loan_amount,
        current_loan_amount=new_approved.current_loan_amount,
        monthly_payment=new_approved.monthly_payment,
        created=time,
        last_updated=time, notes=''
    )

    with Session(engine) as session:
        session.add(approval)
        session.commit()
        created_id = approval.approval_id
    return created_id

def delete_approved_loan(info):
    '''delete approved loan based on user id'''
    with Session(engine) as session:
        approval_loan = session.query(
            Approved_Loans
        ).filter(
            Approved_Loans.email==info.get("email")
        ).first()
        if not approval_loan:
            return None
        session.delete(approval_loan)
        session.commit()
    return 'passed'

def pay_monthly_loan(total, info):
    '''update loan amount based on total passed in param'''
    time = datetime.now()
    loan = {
        "current_loan_amount": total,
        "last_updated":time
    }
    loan = {key: value for key, value in loan.items() if value is not None}
    with Session(engine) as session:
        session.query(
            Approved_Loans
        ).filter(
            Approved_Loans.email==info.get("email")
        ).update(loan)
        session.commit()
    return 'pass'

def update_loan(output, email):
    '''update loan based on new amount due to incurred interest'''
    time = datetime.now()
    loan = {
        "current_loan_amount":output["loan_amount"],
        "monthly_payment":output["monthly_payment"],
        "last_updated":time
    }
    loan = {key: value for key, value in loan.items() if value is not None}
    with Session(engine) as session:
        session.query(
            Approved_Loans
        ).filter(
            Approved_Loans.email==email
        ).update(loan)
        session.commit()
        result = session.query(
            Approved_Loans.loan_id
        ).filter(
            Approved_Loans.email==email
        ).scalar()
    return result
