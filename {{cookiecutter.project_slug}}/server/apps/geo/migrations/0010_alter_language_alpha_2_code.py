# Generated by Django 4.2.3 on 2024-06-27 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("geo", "0009_language_delete_location_country_languages"),
    ]

    operations = [
        migrations.AlterField(
            model_name="language",
            name="alpha_2_code",
            field=models.CharField(max_length=4),
        ),
    ]
