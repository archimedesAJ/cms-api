from rest_framework import serializers

class SendSMSSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=160)
    recipients = serializers.ListField(
        child=serializers.CharField()
    )

class CsvUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.endswith(".csv"):
            raise serializers.ValidationError("Only CSV files are allowed")
        return value


class TemplateSmsSerializer(serializers.Serializer):
    message = serializers.CharField()
    recipients = serializers.DictField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )