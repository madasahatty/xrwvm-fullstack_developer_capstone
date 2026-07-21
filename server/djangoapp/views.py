from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data["userName"]
        password = data["password"]

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({
                "userName": username,
                "status": "Authenticated"
            })

        return JsonResponse({
            "userName": username,
            "status": "Failed"
        })

    return JsonResponse({
        "status": "Only POST method is allowed"
    })


def logout_request(request):
    logout(request)
    return JsonResponse({
        "status": "Logged out"
    })


@csrf_exempt
def registration(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data["userName"]
        password = data["password"]
        first_name = data["firstName"]
        last_name = data["lastName"]
        email = data["email"]

        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "userName": username,
                "status": "Already Registered"
            })

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        login(request, user)

        return JsonResponse({
            "userName": username,
            "status": "Authenticated"
        })

    return JsonResponse({
        "status": "Only POST method is allowed"
    })