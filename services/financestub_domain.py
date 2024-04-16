'''
Finance Stub Domain

Layer where finance stub functions resides
'''
from datetime import datetime
from random import randrange

def generate_apr_credit_score_domain():
    '''Generate apr from random credit score'''
    # Credit Score is a random number from 300-850
    credit_score = randrange(300, 850)

    # Loan APR is predetermined based on credit score
    if credit_score <= 500:
        apr = 15.0
    elif 500 < credit_score <= 600:
        apr = 12.0
    elif 600 < credit_score <= 660:
        apr = 9.6
    elif 660 < credit_score <= 780:
        apr = 7.0
    else:
        apr = 5.6
    return {"credit_score":credit_score,
            "apr":apr}

def check_loan_qualify_domain(info):
    '''check if loan qualifies'''
    income = float(info.get("income"))
    car_price = float(info.get("car_price"))
    down_payment = float(info.get("down_payment"))

    loan_needed = car_price - down_payment

    # The loan can only be approved if the loan is <= 10% of the customer's annual income.
    threshold = income * .10

    # The threshold is only for 1 year, it needs to be * 5 for the course of 5 years.
    approved = 0 if (loan_needed > threshold * 5) else 1
    if approved:
        # generate request
        pass
    return {"approved":approved,
            "max_loan_amount":threshold,
            "actual_loan_amount":loan_needed}

def generate_initial_payment_domain(info):
    '''Generate initial payment based on info'''
    # Default loan is for 5 years, so 60 months initially.
    monthly_payment = round(info / 60, 2)

    return {"loan_amount":info,
            "monthly_payment":monthly_payment}

def generate_required_payment_domain(info):
    '''incur interest based on passed in info'''
    loan_amount = float(info["current_loan_amount"])
    apr = float(info["apr"])
    created = (info["created"])
    last_updated = (info["last_updated"])

    # Calculate Remaining Months For Loan
    # f = '%Y-%m-%d %H:%M:%S'
    created_datetime = created
    last_updated_datetime = last_updated

    # Loan is due 5 years after it was created.
    months_paid = last_updated_datetime - created_datetime
    remaining_months = 60 - (months_paid.days // 30)

    # Update Loan Amount using APR
    updated_loan_amount = round(loan_amount * (1 + (apr/12 * .01)), 2)

    # Update Monthly Pyament based on updated loan
    updated_monthly_payment = round(updated_loan_amount / remaining_months, 2)
    return {"loan_amount":updated_loan_amount,
            "monthly_payment":updated_monthly_payment}

def error_response(message, error_type):
    '''give automated error response'''
    return {"isValid":0,
            "message":message,
            "errorType":error_type,
            "code":406}

def validate_payment(info):
    '''
    validates payment, funnels to the two main validation
    functions
    '''
    if info.get("payment_type") == 0:
        return validate_bank_payment_domain(info)
    return validate_card_payment_domain(info)

def validate_credit_card(card_number: str) -> bool:
    """This function validates a credit card number."""
    # 1. Change datatype to list[int]
    card_number = [int(num) for num in card_number]
    # 2. Remove the last digit:
    check_digit = card_number.pop(-1)
    # 3. Reverse the remaining digits:
    card_number.reverse()
    # 4. Double digits at even indices
    card_number = [num * 2 if idx % 2 == 0
                   else num for idx, num in enumerate(card_number)]
    # 5. Subtract 9 at even indices if digit is over 9
    # (or you can add the digits)
    card_number = [num - 9 if idx % 2 == 0 and num > 9
                   else num for idx, num in enumerate(card_number)]
    # 6. Add the check_digit back to the list:
    card_number.append(check_digit)
    # 7. Sum all digits:
    check_sum = sum(card_number)
    # 8. If checkSum is divisible by 10, it is valid.
    return check_sum % 10 == 0

def validate_card_length_specific(card_company, card_num):
    '''checks if card length satisfies specific company'''
    if card_company == "American Express" and len(card_num) != 15:
        return error_response("Error, card length is not valid for American Express.", 2)
    if card_company in ("Discover", "Mastercard", "Visa") and len(card_num) != 16:
        return error_response("Error, card length is not valid.", 2)
    return {"isValid": 1}

def validate_card_number(card_company, card_num):
    '''Check if card number is valid'''
    if not validate_credit_card(card_num):
        return error_response("Error, card number is not valid.", 3)
    if card_company == "American Express" and card_num[0] != "3":
        return error_response("Error, card number is not valid for American Express.", 4)
    if card_company == "Discover" and card_num[0] != "6":
        return error_response("Error, card number is not valid for Discover.", 4)
    if card_company == "Mastercard" and card_num[0] != "5":
        return error_response("Error, card number is not valid for MasterCard.", 4)
    if card_company == "Visa" and card_num[0] != "4":
        return error_response("Error, card number is not valid for Visa.", 4)
    return {"isValid": 1}

def validate_card_security(card_company, card_cvc):
    '''validates the card security'''
    if card_company in ("Discover", "Mastercard", "Visa") and len(card_cvc) != 3:
        return error_response("Error, the CVC is not valid.", 6)
    if (card_company == "American Express") and len(card_cvc) != 4:
        return error_response("Error, the CVC is not valid for American Express.", 6)
    return {"isValid": 1}

def validate_card_payment_domain(info):
    '''validates the card used'''
    card_company = info.get("company")
    card_num = ''.join(info.get("card_num").split())
    card_exp = info.get("card_exp")
    card_cvc = info.get("card_cvc")

    # Check if card is in the list of accepted cards
    valid_cards = ['American Express', 'Discover', 'Mastercard', 'Visa']
    if card_company not in valid_cards:
        return error_response("Error, card not accepted.", 1)
    response = validate_card_length_specific(card_company, card_num)
    if not response["isValid"]:
        return response
    response = validate_card_number(card_company, card_num)
    if not response["isValid"]:
        return response

    # Check if card expiration date is valid
    exp_month, exp_year = map(int, card_exp.split('/'))
    current_date = datetime.now()
    exp_date = datetime(exp_year, exp_month, 1)

    if exp_date < current_date:
        return error_response("Error, card has expired.", 5)

    response = validate_card_security(card_company, card_cvc)
    if not response["isValid"]:
        return response
    # Check if card security number is valid
    return {"isValid":1,
            "message":"Card Payment Details Verified!",
            "payment_method":info.get("card_num")[-4:],
            "errorType":0}

def validate_account_number(bank, account_number):
    '''Check if account number is valid'''
    if bank == "Wells Fargo" and (len(account_number) < 9 or len(account_number) > 13):
        return error_response("Error, not a valid account number for Wells Fargo.", 2)
    if bank == "Bank of America" and len(account_number) != 12:
        return error_response("Error, not a valid account number for Bank of America.", 2)
    if bank == "Chase" and (len(account_number) < 8 or len(account_number) > 17):
        return error_response("Error, not a valid account number for Chase.", 2)
    if bank == "Citibank" and len(account_number) != 10:
        return error_response("Error, not a valid account number for Citibank.", 2)
    if bank == "PNC" and (len(account_number) < 9 or len(account_number) > 12):
        return error_response("Error, not a valid account number for PNC.", 2)
    return {"isValid": 1}

def validate_routing_number(bank, routing_number):
    '''Check if routing number is valid'''
    if bank == "Wells Fargo" and routing_number != "021200025":
        return error_response("Error, not a valid routing number for Wells Fargo.", 4)
    if bank == "Bank of America" and routing_number != "021200339":
        return error_response("Error, not a valid routing number for Bank of America.", 4)
    if bank == "Chase" and routing_number != "021202337":
        return error_response("Error, not a valid routing number for Chase.", 4)
    if bank == "Citibank" and routing_number != "021272655":
        return error_response("Error, not a valid routing number for Citibank.", 4)
    if bank == "PNC" and routing_number != "031207607":
        return error_response("Error, not a valid routing number for PNC.", 4)
    return {"isValid": 1}

def validate_bank_payment_domain(info):
    '''validates bank payment'''
    bank = info.get("company")
    account_number = info.get("account_number")
    routing_number = info.get("routing_number")

    # Check if bank is in the list of accepted banks
    valid_banks = ['Wells Fargo', 'Bank of America', 'Chase', 'Citibank', 'PNC']
    if bank not in valid_banks:
        return error_response("Error, bank not accepted.", 1)

    response = validate_account_number(bank, account_number)
    if not response["isValid"]:
        return response

    if len(routing_number) != 9:
        return error_response("Error, not a valid routing number length.", 3)
    response = validate_routing_number(bank, routing_number)
    if not response["isValid"]:
        return response

    return{"isValid":1,
            "message":"Bank Payment Details Verified!",
            "payment_method":info.get("account_number")[-4:],
            "errorType":0}
