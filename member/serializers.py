from rest_framework import serializers;
from .models import Member

class MemberSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, required=False, allow_null=True)
    class Meta:
        model = Member
        fields = ['id', 'member_no', 'title', 'full_name',
                  'email', 'gender', 'birthday', 'contact_no', 'image',
                  'location', 'committee', 'department', 'designation'] 
        