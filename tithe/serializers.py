from rest_framework import serializers
from .models import Tithe

# Assuming you have a User model

class TitheSerializer(serializers.ModelSerializer):
    member_details = serializers.SerializerMethodField()

    class Meta:
        model = Tithe
        fields = [
            'id', 'member', 'member_details', 'amount', 'date_given',
            'payment_method', 'contribution_type', 'reference',
            'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'member': {'required': True},
        }

        read_only_fields = ['is_deleted', 'deleted_at']

    def get_member_details(self, obj):
        return {
            "id": obj.member.id,
            "member_no": obj.member.member_no,
            "name": obj.member.full_name,
            "email": obj.member.email,
        }

    def validate_member(self, value):
        if not value:
            raise serializers.ValidationError("Member must be selected.")
        return value
    

    def get_deletion_status(self, obj):
        return "Deleted" if obj.is_deleted else "Active"
    

class MemberTitheSummarySerializer(serializers.Serializer):
    member_id = serializers.IntegerField()
    member_name = serializers.CharField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    tithe_count = serializers.IntegerField()

class MonthlySummarySerializer(serializers.Serializer):
    month = serializers.IntegerField()
    year = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    member_count = serializers.IntegerField()