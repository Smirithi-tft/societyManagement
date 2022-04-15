# Generated by Django 4.0.2 on 2022-04-11 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_customuser_is_admin_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(max_length=40)),
                ('otp_field', models.CharField(max_length=6)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
