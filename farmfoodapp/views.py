import datetime
import pytz
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from farmfoodapp.models import RegisterModel, VendorManager, VendorProduct, VendorInventory
from farmfoodapp.app_serializers import RegisterSerializer, VendorProductSer
from farmfoodapp.actions import check_existing_user, check_login_attempts, reduce_login_attempts, decode_token, \
    send_verification_email, send_forget_pass_email
from rest_framework.decorators import api_view

utc = pytz.UTC


# Create your views here.

@api_view(["POST", "GET"])
def register_api(request):
    try:
        data = request.data
        user_data = data.copy()
        if user_data['user_password'] != user_data['user_password_cnf']:
            return render(request, 'onboarding/User_Registration.html', {'msg': 'Passwords Do Not Match'})
        if check_existing_user(user_data['email']):
            return render(request, 'onboarding/User_Registration.html', {"msg": "User Already Exist"})
        user_data['user_password'] = make_password(user_data['user_password'])
        data_serializer = RegisterSerializer(data=user_data)
        if data_serializer.is_valid():
            data_serializer.save()
            send_verification_email(user_data, user_data['email'])
            return HttpResponse("<h2>Please Check Your Email to Verify your account</h2>")
        else:
            return HttpResponse("SUCCESS")
    except Exception as e:
        return render(request, 'User_Registration.html',
                      {"msg": "Something Went Wrong, Try Again in Some Time, " + str(e)})


@api_view(["POST", "GET"])
def login_api(request):
    try:
        user_data = request.data
        if not check_existing_user(user_data['email']):
            return render(request, 'onboarding/User_Login.html', {"msg": "User Not Registered"})
        data = RegisterModel.objects.get(email=user_data['email'])
        json_data = RegisterSerializer(data)
        json_data = json_data.data
        if data.account_status == "inactive":
            return render(request, 'onboarding/User_Login.html', {"msg": "Account Inactive, Please Confirm Email"})
        attempts, time_lock = check_login_attempts(user_data['email'])
        if attempts == 0:
            return render(request, 'onboarding/User_Login.html', {"msg": "Account Permanently Locked"})
        if not utc.localize(datetime.datetime.now()) > time_lock:
            time_remaining = str(time_lock - utc.localize(datetime.datetime.now()))
            return render(request, 'onboarding/User_Login.html',
                          {"msg": "Account Temporarily Locked, Try Again In " + str(time_remaining[2:4]) + " Minutes"})
        if check_password(user_data['user_password'], data.user_password):
            data.attempts_left = 10
            data.save()
            user_id = data.id
            json_data["id"] = user_id
            request.session["login_session_data"] = json_data
            return HttpResponseRedirect(reverse('home-page'))
        else:
            reduce_login_attempts(user_data['email'], attempts)
            return render(request, 'onboarding/User_Login.html',
                          {"msg": "Login Unsuccessful, Incorrect Password, Attempts Left:" + str(attempts - 1)})
    except Exception as e:
        return HttpResponse("SOMETHING WENT WRONG " + str(e))


def register_view(request):
    return render(request, 'onboarding/User_Registration.html')


def login_view(request):
    if "msg" in request.session:
        msg = {"msg": request.session['msg']}
        del request.session["msg"]
        return render(request, 'onboarding/User_Login.html', msg)
    return render(request, 'onboarding/User_Login.html')

def home_page(request):
    if "login_session_data" in request.session:
        print(request.session["login_session_data"])
        data = VendorProduct.objects.all()
        data_list = [{
            "id": prod.id,
            "product_name": prod.product_name,
            "category": prod.category,
            "description": prod.description,
            "price": float("{:.2f}".format(prod.price)),
            "image": prod.image
        } for prod in data]
        print(data_list)
        return render(request, 'home/HomePage.html',
                      {"products": data_list, "first_name": request.session["login_session_data"]["first_name"]})
    else:
        return HttpResponseRedirect(reverse('login-view'))


@api_view(['GET', 'POST'])
def forget_password_view(request):
    if request.method == "GET":
        return render(request, 'onboarding/User_ForgetPassword.html')
    if request.method == "POST":
        data = request.data
        user_count = RegisterModel.objects.filter(email=data['email']).count()
        if user_count == 0:
            return render(request, 'onboarding/User_ForgetPassword.html', {"msg": "User Does Not Exist"})
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
            return render(request, 'onboarding/User_ResetPassword.html')
        else:
            return HttpResponse("INVALID URL")
    else:
        return HttpResponse("METHOD NOT ALLOWED")


@api_view(['POST'])
def reset_password_api(request):
    if request.method == "POST" and "data" in request.session:
        user_pass = request.data
        if user_pass["user_password"] == user_pass["user_password_cnf"]:
            data = request.session["data"]
            user = RegisterModel.objects.get(email=data['email'])
            user.user_password = make_password(user_pass['user_password'])
            user.save()
            del request.session["data"]
            request.session["msg"] = "Password Reset Successful, Please Login"
            return HttpResponseRedirect(reverse('login-view'))
        else:
            return render(request, 'onboarding/User_ResetPassword.html', {"msg": "Passwords Dont Match"})
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
            request.session["msg"] = "Account Successfully Verified"
            return HttpResponseRedirect(reverse('login-view'))
        else:
            return HttpResponse("<h2>Invalid URL</h2>")
    else:
        return HttpResponse("METHOD NOT ALLOWED")

@api_view(['GET', 'POST'])
def add_product_view(request):
    if request.method == 'GET':
        if "login_session_data" in request.session:
            return render(request, 'products/Add_Product.html')
    if request.method == "POST":
        if "login_session_data" in request.session:
            user_data = request.data
            print(user_data)
            login_data = request.session["login_session_data"]
            vp_obj = VendorProduct(user_id=RegisterModel.objects.get(id=login_data["id"]),
                                   product_name=user_data["product_name"],
                                   category=user_data["category"],
                                   description=user_data["description"],
                                   price=user_data["price"],
                                   image=user_data["image"])
            vp_obj.save()
            return HttpResponse("SUCCESS")