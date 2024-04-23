# Generated by Django 5.0.2 on 2024-02-29 09:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fragments', '0003_sess'),
    ]

    operations = [
        migrations.CreateModel(
            name='payoutData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('current_date_time', models.DateTimeField(auto_now_add=True)),
                ('fragsPaid', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('wzPaid', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
    ]
