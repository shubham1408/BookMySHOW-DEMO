# Generated by Django 3.0.5 on 2020-04-04 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convoapis', '0008_auto_20200404_2134'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.'),
        ),
    ]