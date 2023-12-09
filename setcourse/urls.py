from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("draft/<int:course_id>", views.draft, name="draft"),
    path("new_course", views.new_course, name="new_course"),
    path("profile", views.profile, name="profile"),
    path("dashboard/<int:course_id>", views.dashboard, name="dashboard"),
    path("course/<int:course_id>", views.course, name="course"),
    path("view_messages/<int:module_id>", views.view_messages, name="view_messages"),
    path("new_message", views.new_message, name="new_message"),
]
