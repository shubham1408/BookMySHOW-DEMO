# Generated by Django 3.0.5 on 2020-04-03 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convoapis', '0005_userprofile_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(default='', max_length=250),
        ),
    ]
