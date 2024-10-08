# Generated by Django 4.1 on 2022-09-17 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("geo", "0004_alter_region_iso_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="city",
            name="latitude",
            field=models.DecimalField(decimal_places=6, default=0.0, max_digits=9),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="city",
            name="longitude",
            field=models.DecimalField(decimal_places=6, default=0.0, max_digits=9),
            preserve_default=False,
        ),
    ]
