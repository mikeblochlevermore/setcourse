from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
from django.utils import timezone
import json

from .models import User, Course, Module, Workshop, Comment, Student

# Create your views here.
def index(request):

    return render(request, "setcourse/index.html")


def profile(request):

    draft_courses = Course.objects.filter(host=request.user, published=False)
    published_courses = Course.objects.filter(host=request.user, published=True)

    return render(request, "setcourse/profile.html", {
        "draft_courses": draft_courses,
        "published_courses": published_courses
    })


def course(request, course_id):

    course = Course.objects.get(id=course_id)
    modules = Module.objects.filter(course=course)

    # Gets workshops from modules
    workshops = Workshop.objects.filter(module__in=modules)

    return render(request, "setcourse/course.html", {
        "course": course,
        "modules": modules,
        "workshops": workshops
    })

@csrf_exempt
@login_required
def dashboard(request, course_id):

    if request.method == "GET":

        course = Course.objects.get(id=course_id)
        modules = Module.objects.filter(course=course)

        messages = Comment.objects.filter(module__in=modules)

        return render(request, "setcourse/dashboard.html", {
            "course": course,
            "modules": modules,
            "messages": messages
        })


@csrf_exempt
@login_required
def view_messages (request, module_id):

    if request.method == "GET":

        module = Module.objects.get(id=module_id)
        messages = Comment.objects.filter(module=module)

        messages = messages.order_by("-time").all()
        return JsonResponse([message.serialize() for message in messages], safe=False)


@csrf_exempt
@login_required
def new_message (request):
     if request.method == "POST":

        data = json.loads(request.body)

        message = data["message"]
        module_id = data["module_id"]

        module = Module.objects.get(id=module_id)

        course = Course.objects.get(id=module.course.id)

        if request.user == course.host:
            by_host = True
        else:
            by_host = False

        new_message = Comment.objects.create(
                    module=module,
                    message=message,
                    user=request.user,
                    by_host=by_host,
                )
        new_message.save()

        print(new_message, " - posted")

        return JsonResponse(module.id, safe=False)


def draft (request, course_id):

    course = Course.objects.get(id=course_id)
    modules = Module.objects.filter(course=course)

    # Gets workshops from modules
    workshops = Workshop.objects.filter(module__in=modules)

    return render(request, "setcourse/new_course.html", {
            "course": course,
            "modules": modules,
            "workshops": workshops
        })


@csrf_exempt
def new_course(request):
    if request.method == "GET":

        # Create a blank course
        course = Course.objects.create(
                host=request.user,
            )
        print(f"Course Created. id:", course.id)

        return render(request, "setcourse/new_course.html", {
                "course": course
            })

    if request.method == "PUT":
        data = json.loads(request.body)

        if "new_module" in data and data["new_module"] == "True":

            # lookup the course by id (sent as part of request)
            course = Course.objects.get(id=data["course_id"])

            new_module = Module.objects.create(
                    course=course,
                )
            print(f"Module {new_module.id} - created")
            return JsonResponse(new_module.id, safe=False)

        if "new_workshop" in data and data["new_workshop"] == "True":

            module = Module.objects.get(id=data["module_id"])

            new_workshop = Workshop.objects.create(
                    module=module
                )
            print(f"Workshop {new_workshop.id} - created")
            return JsonResponse(new_workshop.id, safe=False)

        else:

            # lookup the course by id (sent as part of request)
            course = Course.objects.get(id=data["course_id"])

            if "published" in data and data["published"] == "True":
                course.published = True
                course.save()

                print("course", course.title, "-published")
                return HttpResponse(status=204)

            # level = course, module or workshop
            # input = title, description etc.
            # value = data from that input field
            level = data["level"]
            input = data["input"]
            value = data["value"]

            if level == "course":
                setattr(course, input, value)
                course.save()

                print(f"COURSE id: {course.id} detail saved: {input} = {value}")

            if level == "module":
                module = Module.objects.get(id=data["id"])
                setattr(module, input, value)
                module.save()

                print(f"MODULE id: {module.id} detail saved: {input} = {value}")

            if level == "workshop":
                workshop = Workshop.objects.get(id=data["id"])
                setattr(workshop, input, value)
                workshop.save()

                print(f"WORKSHOP id: {workshop.id} detail saved: {input} = {value}")

        return HttpResponse(status=204)

    if request.method == "DELETE":
        data = json.loads(request.body)

        if data["level"] == "course":
            # lookup the module by id (sent as part of request)
            course = Course.objects.get(id=data["id"])
            id = course.id
            course.delete()

            print(f"Course {id} - deleted")


        if data["level"] == "module":

            # lookup the module by id (sent as part of request)
            module = Module.objects.get(id=data["id"])
            id = module.id
            module.delete()

            print(f"Module {id} - deleted")

        if data["level"] == "workshop":

            # lookup the workshop by id (sent as part of request)
            workshop = Workshop.objects.get(id=data["id"])
            id = workshop.id
            workshop.delete()

            print(f"Workshop {id} - deleted")

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
            return HttpResponseRedirect(reverse("profile"))
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