# Generated by Django 4.2.4 on 2023-12-29 00:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0009_customercompany_project_overview_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="project",
            options={"ordering": ["order"], "verbose_name": "Project", "verbose_name_plural": "Projects"},
        ),
        migrations.AddField(
            model_name="project",
            name="order",
            field=models.IntegerField(default=0),
        ),
    ]
