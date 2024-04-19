'''
Loan Data

Layer where all loan related functions talk to the database
'''
# pylint: disable=import-error
from datetime import datetime
from sqlalchemy import and_, desc
from sqlalchemy.orm import Session
from financestub.data.finance_alchemy_setup import engine
from financestub.data.finance_alchemy_classes import Loan_Requests
def create_request(request, notes):
    '''store new loan based on passed in info'''
    time = datetime.now()
    request = Loan_Requests(
        email=request.email,
        credit_score=request.credit_score,
        apr=request.apr,
        vin=request.vin,
        income=request.income,
        car_price=request.total,
        down_payment=request.down_payment,
        max_loan_amount=request.max_loan_amount,
        actual_loan_amount=request.actual_loan_amount,
        approved=request.approved,
        created=time,
        last_updated=time, notes=notes
    )

    with Session(engine) as session:
        session.add(request)
        session.commit()

def get_last_request(info):
    '''get last request, regardless'''
    with Session(engine) as session:
        result=session.query(Loan_Requests
        ).filter(
            Loan_Requests.email==info.get('email')
        ).order_by(
            desc(Loan_Requests.created)
        ).first()
    return result

def get_recent_request(info):
    '''get recent request'''
    with Session(engine) as session:
        result=session.query(Loan_Requests
        ).filter(
            and_(
            Loan_Requests.email==info.get('email'),
            Loan_Requests.approved == 1,
            Loan_Requests.notes==''
            )
        ).order_by(
            desc(Loan_Requests.created)
        ).first()
    return result

def reject_pending(request_id):
    '''rejects all pending requests that are approved'''
    with Session(engine) as session:
        pendings = session.query(Loan_Requests
            ).filter(
                and_(
                    Loan_Requests.request_id != request_id,
                    Loan_Requests.approved == 1
                )
            ).all()
        for pending in pendings:
            time = datetime.now()
            pending.notes="rejected"
            pending.last_updated = time
            session.query(Loan_Requests
                ).filter(
                    Loan_Requests.request_id==pending.request_id
                ).update({
                    Loan_Requests.notes: pending.notes,
                    Loan_Requests.last_updated: pending.last_updated
                })

def update_request(status, request_id):
    '''update request notes with status'''
    time = datetime.now()
    with Session(engine) as session:
        session.query(Loan_Requests).filter(
            Loan_Requests.request_id==request_id
        ).update({Loan_Requests.notes: status,
                  Loan_Requests.last_updated:time})

def clear_user_requests(info):
    '''clear all user requests'''
    with Session(engine) as session:
        query = session.query(Loan_Requests).filter(
            Loan_Requests.email == info.get("email")
        ).all()
        for request in query:
            session.delete(request)
            session.commit()
