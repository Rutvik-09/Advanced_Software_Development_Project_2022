import datetime

from farmfoodapp.models import RegisterModel

lock_timer = {
    7: 10,
    6: 15,
    5: 20,
    4: 25,
    3: 30,
    2: 35,
    1: 40
}


def check_existing_user(email):
    user_count = RegisterModel.objects.filter(email=email).count()
    if user_count == 1:
        return True
    else:
        return False


def check_login_attempts(email):
    attempts_obj = RegisterModel.objects.get(email=email)
    return attempts_obj.attempts_left, attempts_obj.lock


def reduce_login_attempts(email, attempts):
    email_obj = RegisterModel.objects.get(email=email)
    attempts = attempts - 1
    if attempts == 0:
        email_obj.account_status = "locked"
        email_obj.save()
    email_obj.attempts_left = attempts
    email_obj.save()
    if 7 >= attempts >= 1:
        time_obj = datetime.datetime.now() + datetime.timedelta(minutes=lock_timer[attempts])
        email_obj.lock = time_obj
        email_obj.save()
    return True
