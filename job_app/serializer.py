from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from .models import Job
from django.contrib.auth.models import User

# user serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

# Job Serializer
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

# Get Job Serializer
class GetJobSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Job
        fields = ['user', 'title', 'description', 'benefit', 'employment_type', 'job_type', 'is_active', 'is_approved', 'start_date', 'end_date', 'location', 'mobile', 'created_at', 'updated_at', 'updated_by', 'is_deleted']









        