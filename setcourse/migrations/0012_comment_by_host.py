# Generated by Django 4.2.2 on 2023-12-09 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setcourse', '0011_alter_comment_module'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='by_host',
            field=models.BooleanField(default='False'),
        ),
    ]
