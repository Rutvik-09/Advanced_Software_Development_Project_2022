from django.shortcuts import render
from farmfoodapp.models import *

# Create your views here.
from rest_framework.decorators import api_view


@api_view(["POST"])
def register_api(request):
    user_data = request.data
    # To Parse Data
    # register_obj = RegisterModel(user_data)
    # register_obj.save()
    return True


@api_view(["POST"])
def login_api(request):
    user_data = request.data
    return True


@api_view(["POST"])
def reset_secret(request):
    user_data = request.data
    return True


def register_view(request):
    return render(request, 'register.html')
