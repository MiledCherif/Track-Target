# Generated by Django 4.1.7 on 2023-04-07 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_alter_client_tel2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prospet',
            name='tel2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
