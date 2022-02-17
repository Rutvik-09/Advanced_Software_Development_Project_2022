import datetime
import pytz
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from farmfoodapp.models import RegisterModel
from farmfoodapp.app_serializers import RegisterSerializer
from farmfoodapp.actions import check_existing_user, check_login_attempts, reduce_login_attempts
from rest_framework.decorators import api_view

utc = pytz.UTC


# Create your views here.

@api_view(["POST"])
def register_api(request):
    try:
        data = request.data
        if check_existing_user(data['email']):
            return Response(data={"msg": "User Already Exist"}, status=status.HTTP_200_OK)
        user_data = data
        user_data['user_password'] = make_password(data['user_password'])
        data_serializer = RegisterSerializer(data=user_data)
        if data_serializer.is_valid():
            data_serializer.save()
            return Response(data={"msg": "success"}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={"msg": "failed", "error": str(data_serializer.error_messages)},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
    except Exception as e:
        return Response(data={"msg": "failed", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def login_api(request):
    try:
        user_data = request.data
        if not check_existing_user(user_data['email']):
            return Response(data={"msg": "User Not Registered"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        data = RegisterModel.objects.get(email=user_data['email'])
        if data.account_status == "inactive":
            return Response(data={"msg": "Account Inactive, Please Confirm Email"})
        attempts, time_lock = check_login_attempts(user_data['email'])
        if attempts == 0:
            return Response(data={"msg": "Account Permanently Locked"})
        if not utc.localize(datetime.datetime.now()) > time_lock:
            time_remaining = str(time_lock - utc.localize(datetime.datetime.now()))
            return Response(
                data={"Account Temporarily Locked, Try Again In " + time_remaining[2:4] + " Minutes"})
        if check_password(user_data['user_password'], data.user_password):
            data.attempts_left = 10
            data.save()
            return Response(data={"msg": "Login Successful"})
        else:
            reduce_login_attempts(user_data['email'], attempts)
            return Response(data={"msg": "Login Unsuccessful, Incorrect Password, Attempts Left:" + str(attempts - 1)})
    except Exception as e:
        return Response(data={"msg": "failed", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def reset_secret(request):
    # user_data = request.data
    return True


def register_view(request):
    return render(request, 'register.html')
