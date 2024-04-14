'''
Loan Data

Layer where all loan related functions talk to the database
'''
# pylint: disable=import-error
from datetime import datetime
from sqlalchemy import and_, desc
from sqlalchemy.orm import Session
from data.alchemy_setup import engine
from data.alchemy_classes import Loan_Requests
def create_request(request):
    '''store new loan based on passed in info'''
    time = datetime.now()
    request = Loan_Requests(
        email=request.email,
        credit_score=request.credit_score,
        apr=request.apr,
        vin=request.vin,
        income=request.income,
        car_price=request.car_price,
        down_payment=request.down_payment,
        max_loan_amount=request.max_loan_amount,
        actual_loan_amount=request.actual_loan_amount,
        approved=request.approved,
        created=time,
        last_updated=time, notes=''
    )

    with Session(engine) as session:
        session.add(request)
        session.commit()

def get_recent_request(info):
    '''get recent request'''
    with Session(engine) as session:
        result=session.query(Loan_Requests.request_id
        ).filter(
            and_(
            Loan_Requests.email==info.get('email'),
            Loan_Requests.approved == 1
            )
        ).order_by(
            desc(Loan_Requests.created)
        ).first()
    return result
