# Generated by Django 4.2.7 on 2023-12-07 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='zipcode',
            field=models.IntegerField(),
        ),
    ]
