# Generated by Django 4.2.2 on 2023-12-26 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setcourse', '0016_rename_enrolled_student_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='seen',
        ),
    ]
