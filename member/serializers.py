from rest_framework import serializers;
from .models import Member

class MemberSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, required=False, allow_null=True)

    # Optional: Add a read-only field for the full image URL
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Member
        fields = ['id', 'member_no', 'title', 'full_name',
                  'email', 'gender', 'birthday', 'contact_no', 'image',
                  'location', 'committee', 'department', 'designation', 'image_url'] 
        

    def to_representation(self, instance):
        """
        Ensure image field returns the full Cloudinary URL
        """
        data = super().to_representation(instance)
        
        if instance.image:
            # With Cloudinary, this will be a full URL like:
            # https://res.cloudinary.com/your-cloud-name/image/upload/v.../photos/members_photo/image.jpg
            data['image'] = instance.image.url
        
        return data