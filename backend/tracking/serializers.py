# tracking/serializers.py
from rest_framework import serializers
from .models import TrackedObject

class TrackedObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackedObject
        fields = '__all__'
