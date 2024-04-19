'''
SQLAlchemy Classes

Place where all ORM mappings are established for later querying use
'''
# pylint: disable=import-error, too-many-instance-attributes, redefined-builtin, too-many-arguments, too-few-public-methods, invalid-name
from sqlalchemy import (Column, Integer, String,
                        DECIMAL, TIMESTAMP, ForeignKey,
                        Float)
from sqlalchemy.orm import relationship
from data.finance_alchemy_setup import Base

class Loan_Requests(Base):
    '''Loan Requests Class ORM'''
    __tablename__ = "loan_requests"
    request_id = Column(Integer, primary_key = True, autoincrement=True)
    email = Column(String(128))
    credit_score = Column(Integer)
    apr = Column(Float)
    vin = Column(String(17))
    income = Column(DECIMAL(8, 2))
    car_price = Column(DECIMAL(8, 2))
    down_payment = Column(DECIMAL(8, 2))
    max_loan_amount = Column(DECIMAL(8, 2))
    actual_loan_amount = Column(DECIMAL(8, 2))
    approved = Column(Integer)
    created = Column(TIMESTAMP)
    last_updated = Column(TIMESTAMP)
    notes = Column(String(1024))

    approved_request = relationship(
        "Approved_Loans", back_populates="request")

    def __repr__(self):
        return f'''Approval_System(request_id={self.request_id},
                email={self.email}, apr={self.apr},
                credit_score={self.credit_score}, vin={self.vin},
                income={self.income}, car_price={self.car_price},
                down_payment={self.down_payment},
                max_loan_amount={self.max_loan_amount},
                actual_loan_amount={self.actual_loan_amount},
                approved={self.approved},
                created={self.created}, last_updated={self.last_updated},
                notes={self.notes})'''

class Approved_Loans(Base):
    '''Approved Loans Class ORM'''
    __tablename__ = "approved_loans"
    loan_id = Column(Integer, primary_key = True, autoincrement=True)
    request_id = Column(Integer, ForeignKey("loan_requests.request_id"), nullable=False)
    email = Column(String(128))
    vin = Column(String(17))
    apr = Column(Float)
    initial_loan_amount = Column(DECIMAL(8, 2))
    current_loan_amount = Column(DECIMAL(8, 2))
    monthly_payment = Column(DECIMAL(8, 2))
    created = Column(TIMESTAMP)
    last_updated = Column(TIMESTAMP)
    notes = Column(String(1024))

    request = relationship(
        "Loan_Requests", back_populates="approved_request")

    def __repr__(self):
        return f'''Approval_System(loan_id={self.loan_id},
                email={self.email}, vin={self.vin}, apr={self.apr},
                initial_loan_amount={self.initial_loan_amount},
                current_loan_amount={self.current_loan_amount},
                monthly_payment={self.monthly_payment},
                created={self.created}, last_updated={self.last_updated},
                notes={self.notes})'''

class Transactions(Base):
    '''Transactions Class ORM'''
    __tablename__ = "transactions"
    transaction_id = Column(Integer, primary_key = True, autoincrement=True)
    email = Column(String(128), nullable=False)
    vin = Column(String(17))
    amount = Column(DECIMAL(8, 2))
    transaction_type = Column(Integer)
    payment_type = Column(Integer)
    company = Column(String(32))
    payment_method = Column(String(4))
    created = Column(TIMESTAMP)
    last_updated = Column(TIMESTAMP)
    notes = Column(String(1024))

    transactions_transactions_warranties = relationship(
        "Transactions_Warranties", back_populates="transactions")
    transactions_transactions_services = relationship(
        "Transactions_Services", back_populates="transactions")

    def __repr__(self):
        return f'''Approval_System(transaction_id={self.transaction_id},
            email={self.email}, vin={self.vin}, amount={self.amount},
            transaction_type={self.transaction_type}, payment_type={self.payment_type}
            company={self.company}, payment_method={self.payment_method},
            created={self.created},last_updated={self.last_updated}, notes={self.notes})'''

class Transactions_Warranties(Base):
    '''Transactions Warranties Class ORM'''
    __tablename__ = "transactions_warranties"
    transaction_id = Column(Integer, ForeignKey("transactions.transaction_id"), primary_key = True)
    warranty_name = Column(String(32), primary_key = True)
    created = Column(TIMESTAMP)
    last_updated = Column(TIMESTAMP)
    notes = Column(String(1024))

    transactions = relationship(
        "Transactions", back_populates="transactions_transactions_warranties")

    def __repr__(self):
        return f"Transactions_Warranties(transaction_id={self.transaction_id},\
            warranty_name={self.warranty_name}, created={self.created},\
                last_updated={self.last_updated}, notes={self.notes})"

class Transactions_Services(Base):
    '''Transactions Services Class ORM'''
    __tablename__ = "transactions_services"
    transaction_id = Column(Integer, ForeignKey("transactions.transaction_id"), primary_key = True)
    service_name = Column(String(32), primary_key = True)
    created = Column(TIMESTAMP)
    last_updated = Column(TIMESTAMP)
    notes = Column(String(1024))

    transactions = relationship(
        "Transactions", back_populates="transactions_transactions_services")

    def __repr__(self):
        return f"Transactions_Services(transaction_id={self.transaction_id},\
            service_name={self.service_name}, created={self.created},\
                last_updated={self.last_updated}, notes={self.notes})"
