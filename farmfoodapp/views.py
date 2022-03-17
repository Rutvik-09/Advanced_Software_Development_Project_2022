import datetime
import pytz
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
# from rest_framework import status
# from rest_framework.response import Response
from farmfoodapp.models import RegisterModel
from farmfoodapp.app_serializers import RegisterSerializer
from farmfoodapp.actions import check_existing_user, check_login_attempts, reduce_login_attempts, decode_token, send_verification_email, send_forget_pass_email
from rest_framework.decorators import api_view
from rest_framework.response import Response

utc = pytz.UTC


# Create your views here.

@api_view(["POST", "GET"])
def register_api(request):
    try:
        data = request.data
        user_data = data.copy()
        if user_data['user_password'] != user_data['user_password_cnf']:
            return render(request, 'User_Registration.html', {'msg': 'Passwords Do Not Match'})
        if check_existing_user(user_data['email']):
            return render(request, 'User_Registration.html', {"msg": "User Already Exist"})
        user_data['user_password'] = make_password(user_data['user_password'])
        data_serializer = RegisterSerializer(data=user_data)
        if data_serializer.is_valid():
            data_serializer.save()
            send_verification_email(user_data, user_data['email'])
            return HttpResponse("<h2>Please Check Your Email to Verify your account</h2>")
        else:
            return render(request, 'User_Registration.html', {"msg": "Something Went Wrong, Try Again in Some Time"})
    except Exception as e:
        return render(request, 'User_Registration.html',
                      {"msg": "Something Went Wrong, Try Again in Some Time, " + str(e)})


@api_view(["POST", "GET"])
def login_api(request):
    try:
        user_data = request.data
        if not check_existing_user(user_data['email']):
            return render(request, 'User_Login.html', {"msg": "User Not Registered"})
        data = RegisterModel.objects.get(email=user_data['email'])
        if data.account_status == "inactive":
            return render(request, 'User_Login.html', {"msg": "Account Inactive, Please Confirm Email"})
        attempts, time_lock = check_login_attempts(user_data['email'])
        if attempts == 0:
            return render(request, 'User_Login.html', {"msg": "Account Permanently Locked"})
        if not utc.localize(datetime.datetime.now()) > time_lock:
            time_remaining = str(time_lock - utc.localize(datetime.datetime.now()))
            return render(request, 'User_Login.html',
                          {"Account Temporarily Locked, Try Again In " + time_remaining[2:4] + " Minutes"})
        if check_password(user_data['user_password'], data.user_password):
            data.attempts_left = 10
            data.save()
            return HttpResponse("LOGIN SUCCESSFUL")
        else:
            reduce_login_attempts(user_data['email'], attempts)
            return render(request, 'User_Login.html',
                          {"msg": "Login Unsuccessful, Incorrect Password, Attempts Left:" + str(attempts - 1)})
    except Exception as e:
        return HttpResponse("SOMETHING WENT WRONG " + str(e))


def register_view(request):
    return render(request, 'User_Registration.html')


def login_view(request):
    return render(request, 'User_Login.html')


@api_view(['GET', 'POST'])
def forget_password_view(request):
    if request.method == "GET":
        return render(request, 'User_ForgetPassword.html')
    if request.method == "POST":
        data = request.data
        user_count = RegisterModel.objects.filter(email=data['email']).count()
        if user_count == 0:
            return HttpResponse("USER DOES NOT EXIST")
        else:
            user = RegisterModel.objects.get(email=data['email'])
            payload = {
                'email': user.email,
                'phone': user.phone,
            }
            send_forget_pass_email(payload, user.email)
        return HttpResponse("<h1>Please Check Your Email for the RESET URL</h1>")


def reset_password_view(request, token):
    if request.method == "GET":
        result, data = decode_token(token)
        if result:
            request.session["data"] = data
            return render(request, 'User_ResetPassword.html')
        else:
            return HttpResponse("INVALID URL")
    else:
        return HttpResponse("METHOD NOT ALLOWED")


@api_view(['POST'])
def reset_password_api(request):
    if request.method == "POST" and "data" in request.session:
        passwd = request.data
        data = request.session["data"]
        user = RegisterModel.objects.get(email=data['email'])
        user.user_password = make_password(passwd['user_password'])
        user.save()
        del request.session["data"]
        return HttpResponse("Password RESET SUCCESSFULLY")
    else:
        return HttpResponse("METHOD NOT ALLOWED")


def verify_reg_email(request, token):
    if request.method == "GET":
        result, data = decode_token(token)
        if result:
            user = RegisterModel.objects.get(email=data['email'])
            user.account_status = "active"
            user.attempts_left = 10
            user.save()
            return HttpResponseRedirect(reverse('login-view'))
        else:
            return HttpResponse("<h2>Invalid URL</h2>")
    else:
        return HttpResponse("METHOD NOT ALLOWED")


@api_view(['GET'])
def test_api(request):
    data = request.data
    print(data)
    return Response(data={"msg":"success"})