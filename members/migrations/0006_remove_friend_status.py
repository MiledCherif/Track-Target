# Generated by Django 4.1.7 on 2023-04-28 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_profile_friends'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friend',
            name='status',
        ),
    ]
