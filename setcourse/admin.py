from django.contrib import admin
from .models import User, Course, Module, Workshop, Comment, Student

# Register your models here.
admin.site.register(User)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Workshop)
admin.site.register(Comment)
admin.site.register(Student)