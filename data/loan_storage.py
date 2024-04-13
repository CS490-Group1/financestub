'''
Loan Data

Layer where all loan related functions talk to the database
'''
# pylint: disable=import-error
from datetime import datetime
from sqlalchemy.orm import Session
from data.alchemy_setup import engine
from data.alchemy_classes import Approval_System

def grab_approved_loan(info):
    '''grab approved loan based on user id'''
    with Session(engine) as session:
        result = session.query(Approval_System
        ).filter(
            Approval_System.email == info.get("email")
        ).first()
    return result

def store_new_loan(loan):
    '''store new loan based on passed in info'''
    created_id = 0
    time = datetime.now()
    approval = Approval_System(
        email=loan.email,
        credit_score=loan.credit_score,
        apr=loan.apr,
        approved_loan=loan.approved_loan,
        loan_amount=loan.loan_amount,
        monthly_payment=loan.monthly_payment,
        approved=loan.approved,
        created=time,
        last_updated=time, notes=''
    )

    with Session(engine) as session:
        session.add(approval)
        session.commit()
        created_id = approval.approval_id
    return created_id

def update_approval(info):
    '''update approval loan with approved passed in info'''
    time = datetime.now()
    loan = {
        "approved":info.get("approved"),
        "last_updated":time
    }
    with Session(engine) as session:
        session.query(
            Approval_System
        ).filter(
            Approval_System.email==info.get("email")
        ).update(loan)
        session.commit()
        result = session.query(
            Approval_System.approval_id
        ).filter(
            Approval_System.email==info.get("email")
        ).scalar()
    return result

def delete_approved_loan(info):
    '''delete approved loan based on user id'''
    with Session(engine) as session:
        approval_loan = session.query(
            Approval_System
        ).filter(
            Approval_System.email==info.get("email")
        ).first()
        if not approval_loan:
            return None
        session.delete(approval_loan)
        session.commit()
    return 'passed'

def down_payment(info, monthly_payment):
    '''update approval loan with the down payment'''
    time = datetime.now()
    loan = {
        "approved_loan":info.get("approved_loan"),
        "loan_amount":info.get("approved_loan"),
        "monthly_payment":monthly_payment,
        "last_updated":time
    }
    loan = {key: value for key, value in loan.items() if value is not None}
    with Session(engine) as session:
        result = session.query(
            Approval_System.approval_id
        ).filter(
            Approval_System.email==info.get("email")
        ).scalar()
        if not result:
            return "error"
        session.query(
            Approval_System
        ).filter(
            Approval_System.approval_id==result
        ).update(loan)
        session.commit()
    return "success"

def pay_monthly_loan(total, info):
    '''update loan amount based on total passed in param'''
    time = datetime.now()
    loan = {
        "loan_amount": total,
        "last_updated":time
    }
    loan = {key: value for key, value in loan.items() if value is not None}
    with Session(engine) as session:
        session.query(
            Approval_System
        ).filter(
            Approval_System.email==info.get("email")
        ).update(loan)
        session.commit()
    return 'pass'

def update_loan(output, email):
    '''update loan based on new amount due to incurred interest'''
    time = datetime.now()
    loan = {
        "loan_amount":output["loan_amount"],
        "monthly_payment":output["monthly_payment"],
        "last_updated":time
    }
    loan = {key: value for key, value in loan.items() if value is not None}
    with Session(engine) as session:
        session.query(
            Approval_System
        ).filter(
            Approval_System.email==email
        ).update(loan)
        session.commit()
        result = session.query(
            Approval_System.approval_id
        ).filter(
            Approval_System.email==email
        ).scalar()
    return result
