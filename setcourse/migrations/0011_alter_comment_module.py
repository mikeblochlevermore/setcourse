# Generated by Django 4.2.2 on 2023-12-09 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setcourse', '0010_remove_comment_comment_comment_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='setcourse.module'),
        ),
    ]
