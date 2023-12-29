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
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)
    logo = models.ImageField(upload_to='technology')
    experience = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=1)
    type = models.CharField(max_length=50, choices=TechnologyType.choices, default=TechnologyType.OTHER)
    link = models.URLField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-experience']


class Company(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='company')
    link = models.URLField(blank=True)
    put_white_background = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    class Meta:
        abstract = True


class WorkCompany(Company):
    logo = models.ImageField(upload_to='work_company')
    date_from = models.DateField()
    date_to = models.DateField(blank=True, null=True)
    freelance = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class CustomerCompany(Company):
    logo = models.ImageField(upload_to='customer_company')

    def __str__(self):
        return self.name


class Project(models.Model):
    company = models.ForeignKey(WorkCompany, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=False)
    link = models.URLField(blank=True)
    date_from = models.DateField(blank=True)
    date_to = models.DateField(blank=True, null=True)
    technologies = models.ManyToManyField(Technology)
    logo = models.ImageField(upload_to='work_project_logos')
    screenshot = models.ImageField(upload_to='work_project_screenshots', blank=True)
    overview = models.TextField(blank=True)
    customer = models.ForeignKey(CustomerCompany, on_delete=models.CASCADE, blank=True,
                                 null=True)
    order = models.IntegerField(default=0)
    demo_address = models.CharField(blank=True)
    put_white_background = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['order']

    def __str__(self):
        return self.name
