# Generated by Django 4.2.4 on 2023-09-14 05:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_progress'),
    ]

    operations = [
        migrations.AddField(
            model_name='progress',
            name='downloaded_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]