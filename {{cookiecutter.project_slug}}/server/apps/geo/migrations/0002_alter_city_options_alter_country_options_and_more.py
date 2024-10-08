# Generated by Django 4.1 on 2022-09-17 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("geo", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="city",
            options={"verbose_name_plural": "cities"},
        ),
        migrations.AlterModelOptions(
            name="country",
            options={"verbose_name_plural": "countries"},
        ),
        migrations.AlterModelOptions(
            name="currency",
            options={"verbose_name_plural": "currencies"},
        ),
        migrations.AddField(
            model_name="country",
            name="continent",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="geo.continent",
            ),
        ),
    ]
