# Generated by Django 4.2.4 on 2023-12-29 00:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0008_alter_project_company"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomerCompany",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("link", models.URLField(blank=True)),
                ("logo", models.ImageField(upload_to="customer_company")),
                ("description", models.TextField()),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="project",
            name="overview",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="project",
            name="date_from",
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name="project",
            name="screenshot",
            field=models.ImageField(blank=True, upload_to="work_project_screenshots"),
        ),
        migrations.AddField(
            model_name="project",
            name="customer",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="core.customercompany"
            ),
        ),
    ]
