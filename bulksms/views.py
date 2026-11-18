import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .serializers import SendSMSSerializer, CsvUploadSerializer
import csv
import io
from .utils import normalize_ghana_phone

class SendSMSView(APIView):
    def post(self, request):
        serializer = SendSMSSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
        message = serializer.validated_data["message"]
        raw_recipients = serializer.validated_data["recipients"]

        normalized_numbers = []

        for phone in raw_recipients:
            normalized = normalize_ghana_phone(phone)
            if normalized:
                normalized_numbers.append(normalized)

        # Remove duplicates
        normalized_numbers = list(set(normalized_numbers))

        print("Normalized Numbers:", normalized_numbers)

        if not normalized_numbers:
            return Response(
                {"error": "No valid phone numbers found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        payload = {
            "sender": settings.ARK_SENDER_ID,
            "message": message,
            "recipients": normalized_numbers
        }

        headers = {
            "api-key": settings.ARK_API_KEY,
            "Content-Type": "application/json"
        }

        response = requests.post(
            "https://sms.arkesel.com/api/v2/sms/send",
            json=payload,
            headers=headers,
            timeout=10
        )

        print(payload)

        return Response(response.json(), status=response.status_code)
    

class CsvBulkSmsView(APIView):
    def post(self, request):
        serializer = CsvUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        csv_file = serializer.validated_data["file"]
        message = request.data.get("message")

        print("Received CSV file:", csv_file.name)
        print("Message:", message)


        if not message:
            return Response(
                {"error": "Message is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        decoded_file = csv_file.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(decoded_file))

        valid_numbers = []
        invalid_rows = []

        for index, row in enumerate(reader, start=1):
            phone = row.get("Phone Number")
            full_name = row.get("Full Name")

            print("Phone:", phone, "Full Name:", full_name)

            normalized_phone = normalize_ghana_phone(phone)

            print("Normalized Phone:", normalized_phone)

            if normalized_phone:
                valid_numbers.append(normalized_phone)
            else:
                invalid_rows.append({
                    "row": index,
                    "full_name": full_name,
                    "phone_number": phone
                })

        print("Valid Numbers:", valid_numbers)

        if not valid_numbers:
            return Response(
                {"error": "No valid phone numbers found"},
                status=status.HTTP_400_BAD_REQUEST
            )
        


        payload = {
            "sender": settings.ARK_SENDER_ID,
            "message": message,
            "recipients": valid_numbers
        }

        headers = {
            "api-key": settings.ARK_API_KEY,
            "Content-Type": "application/json"
        }

        response = requests.post(
            "https://sms.arkesel.com/api/v2/sms/send",
            json=payload,
            headers=headers,
            timeout=10
        )

        print(payload)

        return Response(response.json(), status=response.status_code)
    

class SendSMSTemplateCSV(APIView):
    def post(self, request):
        serializer = CsvUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        csv_file = serializer.validated_data["file"]
        message = request.data.get("message")

        print("Received CSV file:", csv_file.name)
        print("Message:", message)


        if not message:
            return Response(
                {"error": "Message is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        decoded_file = csv_file.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(decoded_file))

        valid_numbers = []
        invalid_rows = []

        recipients = {}
        
        for index, row in enumerate(reader, start=1):
            phone = row.get("Phone Number")
            full_name = row.get("Full Name")

            normalized_phone = normalize_ghana_phone(phone)

            params = {k: v for k, v in row.items() if k != "Phone Number"}

            recipients[normalized_phone] = params

            if normalized_phone:
                valid_numbers.append(normalized_phone)
            else:
                invalid_rows.append({
                    "row": index,
                    "full_name": full_name,
                    "phone_number": phone
                })

        if not valid_numbers:
            return Response(
                {"error": "No valid phone numbers found"},
                status=status.HTTP_400_BAD_REQUEST
            )
        


        payload = {
            "sender": settings.ARK_SENDER_ID,
            "message": message,
            "recipients": recipients
        }

        headers = {
            "api-key": settings.ARK_API_KEY,
            "Content-Type": "application/json"
        }

        response = requests.post(
            "https://sms.arkesel.com/api/v2/sms/template/send",
            json=payload,
            headers=headers,
            timeout=10
        )

        print(payload)

        return Response(response.json(), status=response.status_code)