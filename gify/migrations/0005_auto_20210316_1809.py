# Generated by Django 3.1.3 on 2021-03-16 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gify', '0004_auto_20210314_1814'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created']},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.CharField(default='Damian', max_length=255),
            preserve_default=False,
        ),
    ]