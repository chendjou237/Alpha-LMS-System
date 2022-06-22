# Generated by Django 2.2 on 2022-06-13 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_auto_20220613_1748'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReturnedBooks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Issue')),
            ],
        ),
    ]