# Generated by Django 4.2.3 on 2023-07-22 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_customer"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
