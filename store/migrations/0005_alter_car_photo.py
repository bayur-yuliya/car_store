# Generated by Django 4.2.6 on 2023-12-13 20:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0004_alter_car_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="car",
            name="photo",
            field=models.ImageField(
                blank=True,
                default="media/default_img/2c8802a0c5f948deddea67614d2ecb63.jpg",
                upload_to="photo/",
            ),
        ),
    ]