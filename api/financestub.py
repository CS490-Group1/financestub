from flask import Flask, request, jsonify, make_response
from random import randrange
from datetime import datetime

app = Flask(__name__)

## This is going to be a simple financal stub for the online car dealership ##

@app.get("/creditcheck")
def test():
    # Credit Score is a random number from 300-850
    creditScore = randrange(300, 850)

    # Loan APR is predetermined based on credit score
    if creditScore <= 500:
        apr = 15.0
    elif creditScore > 500 and creditScore <= 600:
        apr = 12.0
    elif creditScore > 600 and creditScore <= 660:
        apr = 9.6
    elif creditScore > 600 and creditScore <= 780:
        apr = 7.0
    else:
        apr = 5.6 

    return jsonify({"credit_score":creditScore,
                    "apr":apr})

@app.post("/loanqualification")
def loanQualification():
    info = request.json

    income = float(info.get("income"))
    car_price = float(info.get("car_price"))
    down_payment = float(info.get("down_payment"))

    loan_needed = car_price - down_payment

    # The loan can only be approved if the loan is <= 10% of the customer's annual income.
    threshold = income * .10
    
    # The threshold is only for 1 year, it needs to be * 5 for the course of 5 years.
    approved = 0 if (loan_needed > threshold * 5) else 1

    return jsonify({"approved":approved,
                    "loan_approved":loan_needed})
    

@app.post("/initialpayment")
def generateInitialPayment():
    info = request.json

    loan_amount = float(info.get("loan_amount"))

    # Default loan is for 5 years, so 60 months initially.
    monthly_payment = round(loan_amount / 60, 2)

    return jsonify({"loan_amount":loan_amount,
                    "monthly_payment":monthly_payment})

@app.post("/payment")
def generatePayment():
    info = request.json

    loan_amount = float(info.get("loan_amount"))
    apr = float(info.get("apr"))
    created = (info.get("created"))
    last_updated = (info.get("last_updated"))

    # Calculate Remaining Months For Loan
    f = '%Y-%m-%d %H:%M:%S'
    created_datetime = datetime.strptime(created, f)
    last_updated_datetime = datetime.strptime(last_updated, f)

    # Loan is due 5 years after it was created.
    months_paid = last_updated_datetime - created_datetime
    remaining_months = 60 - (months_paid.days // 30)

    # Update Loan Amount using APR
    updated_loan_amount = round(loan_amount * (1 + (apr/12 * .01)), 2)

    # Update Monthly Pyament based on updated loan
    updated_monthly_payment = round(updated_loan_amount / remaining_months, 2)

    return jsonify({"loan_amount":updated_loan_amount,
                    "monthly_payment":updated_monthly_payment})

# @app.post("/validateBankPayment")
# def validateBankPayment()

# @app.post("/validateCardPayment")
# def validateCardPayment()

if __name__ == "__main__":
    app.run(debug=True, port=8001)