from .models import Job
import datetime

# for active job on start date 
def active_job_start_date():
    current_time = datetime.datetime.now()
    jobs = Job.objects.filter(start_date__lte=current_time, is_approved=True, is_deleted=False)
    for j in jobs:
        j.is_active = True
        j.save()

