# Generated by Django 2.2 on 2022-06-17 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0018_book_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='post/'),
        ),
    ]
