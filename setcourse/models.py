from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Course(models.Model):
   host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="course")
   title = models.CharField(max_length=264, default=None)
   description = models.CharField(max_length=1024, default=None)
   practical = models.CharField(max_length=1024, default=None)
   price = models.IntegerField(default=0)
   price_details = models.CharField(max_length=264, default=None)
   links = models.CharField(max_length=1024, default=None)
   time_of_post = models.DateTimeField(auto_now_add=True)

   def serialize(self):
        return {
            "id": self.id,
            "host": f"{self.host}",
            "title": self.title,
            "description": self.description,
            "practical": self.practical,
            "price": self.price,
            "price_details": self.price_details,
            "links": self.links,
            # "time_of_post": self.time_of_post.strftime("%b %d %Y, %I:%M %p"),
        }

# A Module is a section of a Course
# Module dates are calculated by the span of dates in the Class model below
class Module(models.Model):
   course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="module")
   title = models.CharField(max_length=264, default=None)
   description = models.CharField(max_length=1024, default=None)
   location = models.CharField(max_length=1024, default=None)
   notes = models.CharField(max_length=1024, default=None)

   def serialize(self):
        return {
            "id": self.id,
            # "course": f"{self.course}",
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "notes": self.notes,
        }

# A Workshop is a section of a Module
class Workshop(models.Model):
#    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="workshop")
   module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="workshop")
   time = models.DateTimeField(default=None)
   subject = models.CharField(max_length=264, default=None)

   def serialize(self):
        return {
            "id": self.id,
            # "course": f"{self.course}",
            # "module": f"{self.module}",
            "time": self.time.strftime("%b %d %Y, %I:%M %p"),
            "subject": self.subject,
        }


class Comment(models.Model):
   module = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="comment")
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
   time = models.DateTimeField(auto_now_add=True)
   comment = models.CharField(max_length=512, default=None)
   seen = models.BooleanField(default="False")

   def serialize(self):
        return {
            "id": self.id,
            # "module": f"{self.module}",
            "user": f"{self.user}",
            "time": self.time.strftime("%b %d %Y, %I:%M %p"),
            "comment": self.comment,
            "seen": self.seen,
        }


class Student(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student"),
    enrolled = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="student")
    bio_image = models.CharField(max_length=1024, default=None)

    def __str__(self):
        return f"{self.student}, {self.enrolled}, {self.bio_image}"