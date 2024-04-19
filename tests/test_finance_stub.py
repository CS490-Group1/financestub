'''
Test Finance Stub

tests almost all endpoints of finance stub
'''
def test_buy_car_full_success(client):
    '''test buy car with full payment'''
    response = client.post("/buy/car/full", json={
        "email":"creamsicle@gmail.com",
        "vin":"JHMZE2H77ES150185",
        "warranties":["Oil Changes",
                      "Tire Rotation and Alignment",
                      "Battery Replacement"],
        "car_price":38250.00,
        "warranties_cost":123102.00,
        "payment_type":0,
        "transaction_type":0,
        "total":661283.53,
        "company":"Bank of America",
        "account_number":"123123123123",
        "routing_number":"021200339"
    })
    assert response.json["message"] == "Successfully created transaction for car"
    assert response.status_code == 200

def test_buy_car_full_fail(client):
    '''test buy car with full payment'''
    response = client.post("/buy/car/full", json={
        "email":"creamsicle@gmail.com",
        "vin":"JHMZE2H77ES150185",
        "warranties":["Oil Changes",
                      "Tire Rotation and Alignment",
                      "Battery Replacement"],
        "car_price":38250.00,
        "warranties_cost":123102.00,
        "payment_type":0,
        "transaction_type":0,
        "total":661283.53,
        "company":"Bank of America",
        "account_number":"000",
        "routing_number":"021200339"
    })
    assert response.status_code == 406

def test_get_loan_qual_success(client):
    '''test check if loan qualification is successful'''
    response = client.post("/create/request", json={
        "email":"creamsicle@gmail.com",
        "vin":"JHMFA3F29AS538797",
        "total": 142700.00,
        "income": 300000,
        "down_payment": 10000
    })
    assert response.json['approved'] == 1
    assert response.status_code == 202

def test_get_loan_qual_fail(client):
    '''test check if loan qualification fails'''
    response = client.post("/create/request", json={
        "email":"creamsicle@gmail.com",
        "vin":"3D73Y3CL5BG630193",
        "total":142700.00,
        "income": 1000,
        "down_payment": 10000
    })
    assert response.json['approved'] == 0
    assert response.status_code == 201

def test_buy_car_loan_bank(client):
    '''test buying car with loan using bank'''
    response = client.post("/buy/car/loan", json={
        "email":"creamsicle@gmail.com",
        "vin":"JHMFA3F29AS538797",
        "warranties":["Tire Rotation and Alignment",
                      "Battery Replacement",
                      "Brake Inspection"],
        "payment_type":0,
        "transaction_type":1,
        "company":"Bank of America",
        "account_number":"123123123123",
        "routing_number":"021200339",
        "total":30000,
        "down_payment": 30000
    })
    assert response.status_code == 200

def test_buy_services(client):
    '''test buying car with loan using bank'''
    response = client.post("/buy/services", json={
        "email":"creamsicle@gmail.com",
        "vin":"JHMFA3F29AS538797",
        "services":["Tire Rotation and Alignment",
                    "Brake Inspection"],
        "payment_type":0,
        "transaction_type":2,
        "company":"Bank of America",
        "account_number":"123123123123",
        "routing_number":"021200339",
        "total":21000,
        "services_cost":40000,
        "warranties_discount": 20000
    })
    assert response.status_code == 200

def test_monthly_payment_card(client):
    '''test doing monthly payment with card'''
    response = client.patch("/pay/loan", json={
        "email":"creamsicle@gmail.com",
        "vin":"UFACCADG1EH783905",
        "payment_type":1,
        "transaction_type":1,
        "amount":100.50,
        "company":"Visa",
        "card_num":"4490 4978 3645 2232",
        "card_exp":"10/2024",
        "card_cvc":"173"
    })
    assert response.status_code == 201

def test_incurr_interest(client):
    '''test incurring interest after a month'''
    response = client.patch('/incur/interest', json={
        "email":"creamsicle@gmail.com"
    })
    assert response.status_code == 200

def test_remove_approval(client):
    '''test doing monthly payment with card'''
    response = client.post("/get/approved/loan", json={
        "email":"creamsicle@gmail.com"
    })
    assert response.status_code == 200
    remaining = response.json['current_loan_amount']
    print(remaining)
    response = client.patch("/pay/loan", json={
        "email":"creamsicle@gmail.com",
        "vin":"UFACCADG1EH783905",
        "payment_type":1,
        "transaction_type":1,
        "amount":remaining,
        "company":"Visa",
        "card_num":"4490 4978 3645 2232",
        "card_exp":"10/2024",
        "card_cvc":"173"
    })
    assert response.status_code == 201
    response = client.post("/get/approved/loan", json={
        "email":"creamsicle@gmail.com"
    })
    assert response.status_code == 200
    assert response.json is None

def test_get_finance_report(client):
    '''test get finance report'''
    response = client.post("/get/finance/report", json={
        "email":"creamsicle@gmail.com"
    })
    assert len(response.json) > 0
    assert response.status_code == 200

def test_clean_user_transactions(client):
    '''test clean user transactions'''
    response = client.post("/clean/user/transactions", json={
        "email":"creamsicle@gmail.com"
    })
    assert response.status_code == 200

def test_clean_user_requests(client):
    '''test clean user requests'''
    response = client.post("/clean/user/requests", json={
        "email":"creamsicle@gmail.com"
    })
    assert response.status_code == 200
