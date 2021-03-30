# Generated by Django 3.1.3 on 2021-03-22 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20210322_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='facebook_url',
            field=models.URLField(default='', max_length=40),
        ),
        migrations.AlterField(
            model_name='profile',
            name='github_url',
            field=models.URLField(default='', max_length=40),
        ),
        migrations.AlterField(
            model_name='profile',
            name='twitter_url',
            field=models.URLField(default='', max_length=40),
        ),
        migrations.AlterField(
            model_name='profile',
            name='youtube_url',
            field=models.URLField(default='', max_length=40),
        ),
    ]