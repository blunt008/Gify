# Generated by Django 3.1.3 on 2021-03-20 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_profile_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='title',
            field=models.CharField(max_length=40),
        ),
    ]