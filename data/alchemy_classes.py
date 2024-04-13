'''
SQLAlchemy Classes

Place where all ORM mappings are established for later querying use
'''
# pylint: disable=import-error, too-many-instance-attributes, redefined-builtin, too-many-arguments, too-few-public-methods, invalid-name
from sqlalchemy import (Column, Integer, String,
                        Date, DECIMAL, TIMESTAMP, ForeignKey,
                        Float)
from data.alchemy_setup import Base
from sqlalchemy.orm import relationship

class Approval_System(Base):
    '''Approval System Class ORM'''
    __tablename__ = "approval_system"
    approval_id = Column(Integer, primary_key = True, autoincrement=True)
    email = Column(String(128))
    vin = Column(String(17))
    credit_score = Column(Integer)
    apr = Column(Float)
    approved_loan = Column(Integer)
    loan_amount = Column(DECIMAL(8, 2))
    monthly_payment = Column(DECIMAL(8, 2))
    approved = Column(Integer)
    created = Column(TIMESTAMP)
    last_updated = Column(TIMESTAMP)
    notes = Column(String(1024))

    def __repr__(self):
        return f"Approval_System(approved_id={self.approval_id},\
            user_id={self.user_id}, credit_score={self.credit_score},\
                apr={self.apr}, approved_loan={self.approved_loan},\
                    loan_amount={self.loan_amount}, monthly_payment={self.monthly_payment},\
                        approved={self.approved}, created={self.created},\
                            last_updated={self.last_updated}, notes={self.notes})"

class Transactions(Base):
    '''Transactions Class ORM'''
    __tablename__ = "transactions"
    transaction_id = Column(Integer, primary_key = True, autoincrement=True)
    email = Column(String(128), nullable=False)
    amount = Column(DECIMAL(8, 2))
    type = Column(Integer)
    company = Column(String(32))
    payment_method = Column(String(4))
    created = Column(TIMESTAMP)
    last_updated = Column(TIMESTAMP)
    notes = Column(String(1024))

    transactions_transactions_cars = relationship(
        "Transactions_Cars", back_populates="transactions")
    transactions_transactions_warranties = relationship(
        "Transactions_Warranties", back_populates="transactions")
    transactions_transactions_services = relationship(
        "Transactions_Services", back_populates="transactions")

    def __repr__(self):
        return f"Approval_System(transaction_id={self.transaction_id},\
            user_id={self.user_id}, amount={self.amount}, type={self.type},\
                company={self.company}, payment_method={self.payment_method},\
                    created={self.created},last_updated={self.last_updated}, notes={self.notes})"

class Transactions_Cars(Base):
    '''Transactions Cars Class ORM'''
    __tablename__ = "transactions_cars"
    transaction_id = Column(Integer, ForeignKey("transactions.transaction_id"), primary_key = True)
    vin = Column(String(17), primary_key = True)
    created = Column(TIMESTAMP)
    last_updated = Column(TIMESTAMP)
    notes = Column(String(1024))

    transactions = relationship(
        "Transactions", back_populates="transactions_transactions_cars")

    def __repr__(self):
        return f"Approval_System(transaction_id={self.transaction_id}, car_id={self.car_id},\
            created={self.created}, last_updated={self.last_updated}, notes={self.notes})"

class Transactions_Warranties(Base):
    '''Transactions Warranties Class ORM'''
    __tablename__ = "transactions_warranties"
    transaction_id = Column(Integer, ForeignKey("transactions.transaction_id"), primary_key = True)
    warranty = Column(String(32), primary_key = True)
    created = Column(TIMESTAMP)
    last_updated = Column(TIMESTAMP)
    notes = Column(String(1024))

    transactions = relationship(
        "Transactions", back_populates="transactions_transactions_warranties")

    def __repr__(self):
        return f"Transactions_Warranties(transaction_id={self.transaction_id},\
            warranty_id={self.warranty_id}, created={self.created},\
                last_updated={self.last_updated}, notes={self.notes})"

class Transactions_Services(Base):
    '''Transactions Services Class ORM'''
    __tablename__ = "transactions_services"
    transaction_id = Column(Integer, ForeignKey("transactions.transaction_id"), primary_key = True)
    service = Column(String(32), primary_key = True)
    created = Column(TIMESTAMP)
    last_updated = Column(TIMESTAMP)
    notes = Column(String(1024))

    transactions = relationship(
        "Transactions", back_populates="transactions_transactions_services")

    def __repr__(self):
        return f"Transactions_Services(transaction_id={self.transaction_id},\
            service_id={self.service_id}, created={self.created},\
                last_updated={self.last_updated}, notes={self.notes})"
