# Generated by Django 4.1 on 2022-09-18 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0004_order_discount"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="id",
            field=models.PositiveIntegerField(primary_key=True, serialize=False),
        ),
    ]
