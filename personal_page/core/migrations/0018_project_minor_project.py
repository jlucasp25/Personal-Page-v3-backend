# Generated by Django 4.2.4 on 2024-02-18 12:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0017_alter_project_logo_alter_project_screenshot"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="minor_project",
            field=models.BooleanField(blank=True, default=False),
        ),
    ]