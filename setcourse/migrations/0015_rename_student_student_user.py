# Generated by Django 4.2.2 on 2023-12-14 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setcourse', '0014_student_student'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='student',
            new_name='user',
        ),
    ]
