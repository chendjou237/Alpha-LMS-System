# Generated by Django 2.2 on 2022-06-15 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20220615_0247'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='date_of_joining',
            field=models.DateTimeField(auto_now=True),
        ),
    ]