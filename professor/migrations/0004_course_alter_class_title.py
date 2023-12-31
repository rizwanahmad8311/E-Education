# Generated by Django 4.2.4 on 2023-08-21 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('professor', '0003_remove_class_grade_class_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('pf', 'Programming Fundamentals'), ('isl', 'Islamic Studies')], max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='class',
            name='title',
            field=models.CharField(choices=[('IT', 'Information Technology'), ('SE', 'Software Engineering'), ('CS', 'Computer Science'), ('CE', 'Computer Engineering')], max_length=20),
        ),
    ]
