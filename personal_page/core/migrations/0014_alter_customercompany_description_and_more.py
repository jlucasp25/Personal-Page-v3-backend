# Generated by Django 4.2.4 on 2023-12-29 15:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0013_alter_technology_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customercompany",
            name="description",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="workcompany",
            name="description",
            field=models.TextField(blank=True),
        ),
    ]
