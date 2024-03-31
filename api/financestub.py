from flask import Flask, request, jsonify, make_response
from random import randrange

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

    return jsonify({"credit_score":creditScore, "APR":apr})

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

    return jsonify({"approved":approved})
    

# @app.post("/monthlypayments")
# def generatePayments(info)

# @app.post("/validateBankPayment")
# def validateBankPayment(info)

# @app.post("/validateCardPayment")
# def validateCardPayment(info)

if __name__ == "__main__":
    app.run(debug=True, port=8001)