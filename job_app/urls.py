
from django.urls import path
from .views import create_job, get_all_active_jobs, update_job, delete_job, approve_job_by_admin, get_pending_job_by_admin, get_all_my_jobs

urlpatterns = [
    path('create_job/', create_job),
    path('get_all_active_jobs/', get_all_active_jobs),
    path('get_all_my_jobs/', get_all_my_jobs),
    path('update_job/', update_job),
    path('delete_job/', delete_job),
    path('approve_job_by_admin/', approve_job_by_admin),
    path('get_pending_job_by_admin/', get_pending_job_by_admin),

]
