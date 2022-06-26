from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Job(models.Model):
    job_choices=[
        ('Remote', 'Remote'),
        ('Part Time', 'Part Time'),
        ('Full Time', 'Full Time'),
        ('Contract Base','Contract Base')
    ]
    employee_choices=[
        ('Entry', 'Entry'),
        ('Junior', 'Junior'),
        ('Middle', 'Middle'),
        ('Senior', 'Senior'),
      
    ]

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=512, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    benefit = models.TextField(null=True, blank=True)
    employment_type = models.CharField(max_length=30,choices=employee_choices, null=True, blank=True)
    job_type=models.CharField(max_length=255, choices=job_choices ,null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    mobile = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.CharField(max_length=64, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title


    class Meta:
        db_table = 'Job'