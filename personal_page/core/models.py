from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Activity(models.Model):
    class ActivityType(models.TextChoices):
        WORK = "WORK", "Work"
        FREELANCE = "FREELANCE", "Freelance"
        OTHER = "OTHER", "Other"

    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=255, choices=ActivityType.choices)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Technology(models.Model):
    class TechnologyType(models.TextChoices):
        BACKEND = "BACKEND", "Backend"
        FRONTEND = "FRONTEND", "Frontend"
        MOBILE = "MOBILE", "Mobile"
        DEVOPS = "DEVOPS", "DevOps"
        DATABASE = "DATABASE", "Database"
        OTHER = "OTHER", "Other"

    title = models.CharField(max_length=255)
    description = models.TextField()
    active = models.BooleanField(default=False)
    logo = models.ImageField(upload_to='technology')
    experience = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=1)
    type = models.CharField(max_length=50, choices=TechnologyType.choices, default=TechnologyType.OTHER)
    link = models.URLField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-experience']


class WorkCompany(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='work_company')
    link = models.URLField(blank=True)
    date_from = models.DateField()
    date_to = models.DateField(blank=True, null=True)
    description = models.TextField()
    freelance = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Project(models.Model):
    company = models.ForeignKey(WorkCompany, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField(blank=True)
    date_from = models.DateField()
    date_to = models.DateField(blank=True, null=True)
    technologies = models.ManyToManyField(Technology)
    logo = models.ImageField(upload_to='work_project_logos')
    screenshot = models.ImageField(upload_to='work_project_screenshots')

    def __str__(self):
        return self.name

