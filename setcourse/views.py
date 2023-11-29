from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
from django.utils import timezone
import json

from .models import User, Course, Module, Workshop, Comment, Student

# Create your views here.
def index(request):
    return render(request, "setcourse/index.html")


@csrf_exempt
def new_course(request):
    if request.method == "GET":

        # Create a blank course
        new_course = Course.objects.create(
                host=request.user,
            )
        print(f"Course Created. id:", new_course.id)

        return render(request, "setcourse/new_course.html", {
                "id": new_course.id
            })

    if request.method == "PUT":
        data = json.loads(request.body)
        # lookup the course by id (sent as part of request)
        course = Course.objects.get(id=data["course_id"])

        # level = course, module or workshop
        # input = title, description etc.
        # new_value = data from that input field
        level = data["level"]
        input = data["input"]
        new_value = data["new_value"]

        if level == "course":
            setattr(course, input, new_value)
            course.save()

            print("new detail saved")

        return HttpResponse(status=204)




def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "setcourse/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "setcourse/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "setcourse/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "setcourse/register.html")