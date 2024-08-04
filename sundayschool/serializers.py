from rest_framework import serializers
from .models import SundaySchool

class SundaySchoolSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)
    class Meta:
        model = SundaySchool
        fields='__all__'