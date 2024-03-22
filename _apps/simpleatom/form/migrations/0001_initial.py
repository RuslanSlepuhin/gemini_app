# Generated by Django 5.0.1 on 2024-03-10 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomFormModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_name', models.CharField(max_length=100)),
                ('message', models.CharField(max_length=100)),
                ('questions', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='FormAnswerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField(blank=True, null=True)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
