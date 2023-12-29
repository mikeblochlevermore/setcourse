# Generated by Django 4.2.2 on 2023-12-29 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setcourse', '0017_remove_comment_seen'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='course',
        ),
        migrations.AddField(
            model_name='student',
            name='courses',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='student', to='setcourse.course'),
        ),
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.CharField(default='https://images.pexels.com/photos/1037996/pexels-photo-1037996.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', max_length=264, null=True),
        ),
    ]
