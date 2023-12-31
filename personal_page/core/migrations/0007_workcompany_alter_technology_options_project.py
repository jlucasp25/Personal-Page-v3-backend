# Generated by Django 4.2.4 on 2023-08-18 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0006_technology_link"),
    ]

    operations = [
        migrations.CreateModel(
            name="WorkCompany",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("logo", models.ImageField(upload_to="work_company")),
                ("link", models.URLField(blank=True)),
                ("date_from", models.DateField()),
                ("date_to", models.DateField(blank=True, null=True)),
                ("description", models.TextField()),
                ("freelance", models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterModelOptions(
            name="technology",
            options={"ordering": ["-experience"]},
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("link", models.URLField(blank=True)),
                ("date_from", models.DateField()),
                ("date_to", models.DateField(blank=True, null=True)),
                ("logo", models.ImageField(upload_to="work_project_logos")),
                ("screenshot", models.ImageField(upload_to="work_project_screenshots")),
                ("company", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.workcompany")),
                ("technologies", models.ManyToManyField(to="core.technology")),
            ],
        ),
    ]
