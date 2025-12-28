from rest_framework import serializers
from backend_apps.media.models import Image, Sound


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("public_id", "path_file")


class SoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sound
        fields = ("public_id", "path_file")
