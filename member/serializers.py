from rest_framework import serializers;
from .models import Member
import cloudinary.uploader
from cloudinary.exceptions import Error as CloudinaryError

class MemberSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, required=False, allow_null=True)
    image_url = serializers.ReadOnlyField()
    class Meta:
        model = Member
        fields = ['id', 'member_no', 'title', 'full_name',
                  'email', 'gender', 'birthday', 'contact_no', 'image', 'image_url',
                  'location', 'committee', 'department', 'designation'] 
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop("image")

        return representation