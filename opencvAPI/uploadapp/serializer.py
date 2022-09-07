from django.db.models import FileField
from rest_framework import serializers
from opencvAPI import settings

from uploadapp.models import File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"