from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .serializer import JobSerializer, GetJobSerializer
from .models import Job
import datetime
from django.contrib.auth.models import User
# Create your views here.

# create job api
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_job(request):
    user = request.user
    title = request.data['title'] if 'title' in request.data else None
    description = request.data['description'] if 'description' in request.data else None
    location = request.data['location'] if 'location' in request.data else None
    start_date = request.data['start_date'] if 'start_date' in request.data else None
    if not title or not description  or not location or not start_date:
        return Response({'success': False, 'response': {'message': "Invalid Data!" }},
                    status=status.HTTP_400_BAD_REQUEST)
    request.data._mutable = True
    request.data['user'] = str(user.id)
    serializer = JobSerializer(data=request.data)
    if serializer.is_valid():
        job = serializer.save()
        serializer = GetJobSerializer(job)
        return Response({'success': True, 'response': {'message': serializer.data}},
                    status=status.HTTP_201_CREATED)
    return Response({'success': False, 'response': {'message': serializer.errors}},
                    status=status.HTTP_400_BAD_REQUEST)

# get my uploaded jobs api(active and inactive both) 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_my_jobs(request):
    user  = request.user
    jobs = Job.objects.filter(user=user, is_deleted=False).order_by("-created_at")
    serializer = GetJobSerializer(jobs, many=True)
    return Response({'success': True, 'response': {'message': serializer.data}},
                    status=status.HTTP_200_OK)

# get all active jobs api
@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_active_jobs(request):
    jobs = Job.objects.filter(is_approved=True, is_active=True, is_deleted=False).order_by("-created_at")
    serializer = GetJobSerializer(jobs, many=True)
    return Response({'success': True, 'response': {'message': serializer.data}},
                    status=status.HTTP_200_OK)

    
# update job api
@api_view(['PUT'])
@permission_classes([AllowAny])
def update_job(request):
    id = request.data['id'] if 'id' in request.data else None
    user = request.user
    if not id:
        return Response({'success': False, 'response': {'message': "Provide Job Id" }},
            status=status.HTTP_400_BAD_REQUEST)
    try:
        job = Job.objects.get(id=id, is_deleted=False)
    except Exception as e:
        return Response({"success": False, 'response': {'message': str(e)}},
                        status=status.HTTP_404_NOT_FOUND)
    if job.user != user:
        return Response({'success': False, 'response': {'message': 'You are not authorized to update this job.'}},
                    status=status.HTTP_403_FORBIDDEN)    
    serializer = JobSerializer(job, data=request.data, partial=True)
    if serializer.is_valid():
        job = serializer.save()
        serializer = GetJobSerializer(job)
        return Response({'success': True, 'response': {'message': serializer.data}},
                    status=status.HTTP_200_OK)
    return Response({'success': False, 'response': {'message': serializer.errors}},
                    status=status.HTTP_400_BAD_REQUEST)

# delete job api
@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_job(request):
    id = request.data['id'] if 'id' in request.data else None
    user = request.user
    if not id:
        return Response({'success': False, 'response': {'message': "Provide Job Id" }},
            status=status.HTTP_400_BAD_REQUEST)
    try:
        job = Job.objects.get(id=id, is_deleted=False)
    except Exception as e:
        return Response({'success': False, 'response': {'message': str(e)}},
                    status=status.HTTP_404_NOT_FOUND)
    if job.user != user:
        return Response({'success': False, 'response': {'message': 'You are not authorized to delete this job.'}},
                    status=status.HTTP_403_FORBIDDEN)  
    job.is_deleted = True
    job.save()
    return Response({'success': True, 'response': {'message': "Job Deleted Successfully"}},
                status=status.HTTP_200_OK)

# get pending job api for admin
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_pending_job_by_admin(request):
    jobs = Job.objects.filter(is_approved=False, is_active=False, is_deleted=False).order_by("-created_at")
    serializer = GetJobSerializer(jobs, many=True)
    return Response({'success': True, 'response': {'message': serializer.data}},
                    status=status.HTTP_200_OK)

# approve job by admin api
@api_view(['PUT'])
@permission_classes([IsAdminUser])
def approve_job_by_admin(request):
    id = request.data['id'] if 'id' in request.data else None
    user = request.user
    if not id:
        return Response({'success': False, 'response': {'message': "Provide Job Id" }},
            status=status.HTTP_400_BAD_REQUEST)
    try:
        job = Job.objects.get(id=id, is_deleted=False, is_approved=False, is_active=False)
    except Exception as e:
        return Response({'success': False, 'response': {'message': str(e)}},
                    status=status.HTTP_404_NOT_FOUND)
    job.is_approved = True
    job.updated_by = str(user)
    job.updated_at = datetime.datetime.now()
    job.save()
    return Response({'success': True, 'response': {'message': "Job Approved Successfully"}},
                status=status.HTTP_200_OK)