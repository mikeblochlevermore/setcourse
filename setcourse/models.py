from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Course(models.Model):
   host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="course")
   title = models.CharField(max_length=264, default=None, null=True)
   image = models.CharField(max_length=264, default="https://images.pexels.com/photos/1037996/pexels-photo-1037996.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2", null=True)
   description = models.CharField(max_length=1024, default=None, null=True)
   practical = models.CharField(max_length=1024, default=None, null=True)
   price = models.IntegerField(default=0, null=True)
   price_details = models.CharField(max_length=264, default=None, null=True)
   links = models.CharField(max_length=1024, default=None, null=True)
   time_of_post = models.DateTimeField(auto_now_add=True, null=True)
   published = models.BooleanField(default="False")

   def serialize(self):
        return {
            "id": self.id,
            "host": f"{self.host}",
            "title": self.title,
            "image": self.image,
            "description": self.description,
            "practical": self.practical,
            "price": self.price,
            "price_details": self.price_details,
            "links": self.links,
            "published": self.published,
            # "time_of_post": self.time_of_post.strftime("%b %d %Y, %I:%M %p"),
        }

# A Module is a section of a Course
# Module dates are calculated by the span of dates in the Class model below
class Module(models.Model):
   course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="module")
   title = models.CharField(max_length=264, default=None, null=True)
   description = models.CharField(max_length=1024, default=None, null=True)
   location = models.CharField(max_length=1024, default=None, null=True)
   start_date = models.DateField(default=None, null=True)
   end_date = models.DateField(default=None, null=True)
   notes = models.CharField(max_length=1024, default=None, null=True)

   def serialize(self):
        return {
            "id": self.id,
            # "course": f"{self.course}",
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "notes": self.notes,
        }

# A Workshop is a section of a Module
class Workshop(models.Model):
   module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="workshop")
   start_time = models.DateTimeField(default=None, null=True)
   end_time = models.DateTimeField(default=None, null=True)
   subject = models.CharField(max_length=264, default=None, null=True)

   def serialize(self):
        return {
            "id": self.id,
            "start_time": self.start_time.strftime("%Y-%m-%dT%H:%M"),
            "end_time": self.end_time.strftime("%Y-%m-%dT%H:%M"),
            "subject": self.subject,
        }


class Comment(models.Model):
   module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="comment")
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
   time = models.DateTimeField(auto_now_add=True)
   message = models.CharField(max_length=2048, default=None)
   by_host = models.BooleanField(default="False")

   def serialize(self):
        return {
            "id": self.id,
            "user": f"{self.user}",
            "time": self.time.strftime("%b %d %Y, %I:%M %p"),
            "message": self.message,
            "by_host": self.by_host
        }


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student", default=None)
    courses = models.ManyToManyField(Course, related_name="student", blank=True, default=None)

    def __str__(self):
        return f"{self.user}, {self.courses}"