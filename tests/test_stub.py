from tests.conftest import client

def testCreditCheck(client):
    response = client.get("/creditcheck")
    assert response.status_code == 200

    data = response.json
    assert "credit_score" in data
    assert "apr" in data
    assert 300 <= data.get("credit_score") <= 850

def testLoanQualificationSuccess(client):
    response = client.post("/loanqualification", json={
        "income": "150000",
        "car_price": "50000",
        "down_payment": "10000"
    })
    assert response.status_code == 200

    data = response.json
    assert data.get("approved") == 1

def testLoanQualificationFailed(client):
    response = client.post("/loanqualification", json={
        "income": "50000",
        "car_price": "50000",
        "down_payment": "10000"
    })
    assert response.status_code == 200

    data = response.json
    assert data.get("approved") == 0

def testInitialPayment1(client):
    response = client.post("/initialpayment", json={
        "loan_amount":5500
    })
    assert response.status_code == 200

    data = response.json
    assert "monthly_payment" in data
    assert data.get("monthly_payment") == 91.67

def testInitialPayment2(client):
    response = client.post("/initialpayment", json={
        "loan_amount":10000
    })
    assert response.status_code == 200

    data = response.json
    assert "monthly_payment" in data
    assert data.get("monthly_payment") == round(10000/60, 2)

def testPayment(client):
    response = client.post("/payment", json={
        "loan_amount": "5408.33",
        "apr": 12.0,
        "created": "2024-03-31 00:59:43",
        "last_updated": "2024-04-30 00:59:43"
    })
    assert response.status_code == 200

    data = response.json
    assert "loan_amount" in data
    assert "monthly_payment" in data
    assert data.get("loan_amount") == 5462.41
    assert data.get("monthly_payment") == 92.58

def testValidateBankPaymentSuccess(client):
    response = client.post("/validatebankpayment", json={
        "bank":"Bank of America",
        "account_number":"123123123123",
        "routing_number":"021200339"
    })
    assert response.status_code == 200

    data = response.json
    assert data.get("isValid") == 1

def testValidateBankPaymentFail1(client):
    response = client.post("/validatebankpayment", json={
        "bank":"Wells Fargo",
        "account_number":"123123123123",
        "routing_number":"021200339"
    })
    assert response.status_code == 406

    data = response.json
    assert data.get("isValid") == 0
    assert data.get("message") == "Error, not a valid routing number for Wells Fargo."

def testValidateBankPaymentFail2(client):
    response = client.post("/validatebankpayment", json={
        "bank":"Karanicles of Narnia",
        "account_number":"123123123123",
        "routing_number":"021200339"
    })
    assert response.status_code == 406

    data = response.json
    assert data.get("isValid") == 0
    assert data.get("message") == "Error, bank not accepted."

def testValidateCardPaymentSuccess(client):
    response = client.post("/validatecardpayment", json={
        "card_company":"Visa",
        "card_num":"4490 4978 3645 2232",
        "card_exp":"10/2024",
        "card_cvc":"173"
    })
    assert response.status_code == 200

    data = response.json
    assert data.get("isValid") == 1

def testValidateCardPaymentFail1(client):
    response = client.post("/validatecardpayment", json={
        "card_company":"American Express",
        "card_num":"4490 4978 3645 2232",
        "card_exp":"10/2024",
        "card_cvc":"173"
    })
    assert response.status_code == 406

    data = response.json
    assert data.get("isValid") == 0
    assert data.get("message") == "Error, card length is not valid for American Express."

def testValidateCardPaymentFail2(client):
    response = client.post("/validatecardpayment", json={
        "card_company":"Discover",
        "card_num":"4490 4978 3645 2232",
        "card_exp":"10/2024",
        "card_cvc":"173"
    })
    assert response.status_code == 406

    data = response.json
    assert data.get("isValid") == 0
    assert data.get("message") == "Error, card number is not valid for Discover."

def testValidateCardPaymentFail3(client):
    response = client.post("/validatecardpayment", json={
        "card_company":"Visa",
        "card_num":"4490 4978 3645 2232",
        "card_exp":"10/2022",
        "card_cvc":"173"
    })
    assert response.status_code == 406

    data = response.json
    assert data.get("isValid") == 0
    assert data.get("message") == "Error, card has expired."


