# Generated by Django 4.2.2 on 2023-06-25 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0004_alter_order_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="items",
        ),
        migrations.AddField(
            model_name="order",
            name="items",
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.CASCADE, to="app.item"
            ),
            preserve_default=False,
        ),
    ]
