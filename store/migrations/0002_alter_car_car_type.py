# Generated by Django 4.2.6 on 2023-10-21 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="car",
            name="car_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="store.cartype"
            ),
        ),
    ]
