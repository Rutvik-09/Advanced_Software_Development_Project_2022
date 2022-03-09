import datetime
import jwt

from farmfoodapp.models import RegisterModel
from farmfoodapp.send_mail import send_email

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


def create_token(payload):
    encoded_jwt = jwt.encode(payload, "group13secret", algorithm="HS256")
    return encoded_jwt


def decode_token(token):
    try:
        data = jwt.decode(token, "group13secret", algorithms=["HS256"])
        return True, data
    except Exception:
        return False


def send_forget_pass_email(payload, email):
    token = create_token(payload)
    url = "http://localhost:8000/reset/" + token
    subject = "Farm n Food - Reset Password"
    body = f"""
        <h2>You or Someone has Requested to Reset Your Password</h1>
        <h3>Please Click on the below URL to Reset Password</h3>
        {url}
        """
    send_email(subject, body, email)
    return True


def send_verification_email(payload, email):
    token = create_token(payload)
    url = "http://localhost:8000/verify/" + token
    subject = "Farm n Food - Verify Email"
    body = f"""
    <h2>Please Verify Your Email </h1>
    <h3>Please Click on the below URL to Verify</h3>
    {url}
    """
    send_email(subject, body, email)
    return True
