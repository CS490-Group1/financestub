from services.approved_loans import get_approved_loan


def get_user_approved_loan_app(info):
    '''delete all info relating to user'''
    return get_approved_loan(info)