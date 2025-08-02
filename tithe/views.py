from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Tithe
from .serializers import TitheSerializer
from django_filters.rest_framework import DjangoFilterBackend, DateFilter, FilterSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO
import datetime
from collections import defaultdict
from django.db.models import Sum, Count
from django.utils import timezone
from rest_framework.views import APIView
from .serializers import MemberTitheSummarySerializer, MonthlySummarySerializer


class TitheFilter(FilterSet):
    date_given__gte = DateFilter(field_name='date_given', lookup_expr='gte', label='Date (Greater than or equal)')
    date_given__lte = DateFilter(field_name='date_given', lookup_expr='lte', label='Date (Less than or equal)')
    
    class Meta:
        model = Tithe
        fields = {
            'member': ['exact'],
            'contribution_type': ['exact'],
            'payment_method': ['exact'],
        }


class TitheViewSet(viewsets.ModelViewSet):

    filter_backends = [DjangoFilterBackend]  # Add this
    filterset_fields = ['member']  # Enable member filtering

    queryset = Tithe.objects.filter(is_deleted=False)
    serializer_class = TitheSerializer

    authentication_classes = [JWTAuthentication]  # Add JWT authentication
    permission_classes = [IsAuthenticated]  # Require authentication for all actions


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "status": "success",
                "message": "Tithe recorded successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
    

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "status": "success",
                "message": "Tithe updated successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,headers=headers
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {
                "status": "success",
                "message": "Tithe marked as deleted.",
                "data": None,
            },
            status=status.HTTP_204_NO_CONTENT,
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        if not serializer.data:
            return Response(
            {
                "status": "error",
                "message": "No tithe data found",
                "data": serializer.data,
            },
            status=status.HTTP_404_NOT_FOUND,
        )
        else:
            return Response(
                {
                    "status": "success",
                    "message": "Tithes retrieved successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {
                "status": "success",
                "message": "Tithe details retrieved.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
    
    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        """Admin-only endpoint to restore deleted tithes"""
        tithe = self.get_object()
        if not tithe.is_deleted:
            return Response(
                {"status": "error", "message": "Record is not deleted."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        tithe.is_deleted = False
        tithe.deleted_at = None
        tithe.save()
        
        serializer = self.get_serializer(tithe)
        return Response(
            {
                "status": "success",
                "message": "Tithe restored successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    
     # Add to views.py - to view all deleted tithes
    @action(detail=False, methods=['get'])
    def deleted(self, request):
        deleted_tithes = Tithe.objects.filter(is_deleted=True)
        serializer = self.get_serializer(deleted_tithes, many=True)
        return Response(serializer.data)
    

    #view tithes by specific member
    @action(detail=False, methods=['get'], url_path='by-member/(?P<member_id>[^/.]+)')
    def by_member(self, request, member_id=None):
        """
        Get all tithes for a specific member.
        Admin can view any member's tithes.
        """
        tithes = Tithe.objects.filter(member_id=member_id, is_deleted=False)
        
        if not tithes.exists():
            return Response(
                {
                    "status": "error",
                    "message": "No tithes found for this member.",
                    "data": []
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(tithes, many=True)
        return Response(
            {
                "status": "success",
                "message": f"Tithes retrieved for member ID {member_id}",
                "data": serializer.data,
                "meta": {
                    "total_tithes": tithes.count(),
                    "total_amount": sum(t.amount for t in tithes),
                    "date_range": {
                        "start": request.query_params.get('date_given__gte'),
                        "end": request.query_params.get('date_given__lte')
                    }
                }
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'], url_path='export-pdf/(?P<member_id>[^/.]+)')
    def export_pdf(self, request, member_id=None):
        """Generate PDF report for a member's tithes"""
        tithes = self.filter_queryset(
            self.get_queryset().filter(member_id=member_id)
        ).order_by('date_given')

        if not tithes.exists():
            return Response(
                {"status": "error", "message": "No tithes to export."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Create PDF
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        
        # PDF Content
        member = tithes.first().member
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, 800, f"Tithe Report for {member.full_name}")
        p.setFont("Helvetica", 12)
        p.drawString(100, 775, f"Report Date: {datetime.datetime.now()}")
        
        # Date range info if filtered
        date_start = request.GET.get('date_given__gte')
        date_end = request.GET.get('date_given__lte')
        if date_start or date_end:
            p.drawString(100, 750, f"Period: {date_start or 'N/A'} to {date_end or 'N/A'}")
            y_position = 725
        else:
            y_position = 750
        
        # Table Header
        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, y_position, "Date")
        p.drawString(200, y_position, "Type")
        p.drawString(300, y_position, "Amount")
        p.drawString(400, y_position, "Method")
        y_position -= 20
        
        # Table Rows
        p.setFont("Helvetica", 10)
        for tithe in tithes:
            p.drawString(100, y_position, str(tithe.date_given))
            p.drawString(200, y_position, tithe.get_contribution_type_display())
            p.drawString(300, y_position, f"GHS{tithe.amount}")
            p.drawString(400, y_position, tithe.get_payment_method_display())
            y_position -= 15

        # Footer with totals
        p.setFont("Helvetica-Bold", 12)
        p.drawString(300, y_position - 20, f"Total: GHS{sum(t.amount for t in tithes)}")
        
        p.showPage()
        p.save()
        
        # Prepare response
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        filename = f"tithe_report_{member_id}_{datetime.datetime.now()}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

class TitheAnalyticsView(APIView):
    permission_classes =  [IsAuthenticated]

    def get(self, request):
        try:
            year = int(request.query_params.get('year', timezone.now().year))
            month = int(request.query_params.get('month')) if request.query_params.get('month') else None
        except ValueError:
            return Response(
                {"status": "error", "message": "Invalid year/month format"},
                status=400
            )

        # Base queryset
        tithes = Tithe.objects.filter(is_deleted=False)
        
        # Apply year/month filters if provided
        if year:
            tithes = tithes.filter(date_given__year=year)
        if month:
            tithes = tithes.filter(date_given__month=month)

        # 1. Total Summary
        total_summary = tithes.aggregate(
            total_amount=Sum('amount'),
            member_count=Count('member', distinct=True)
        )

        # 2. By Member
        by_member = tithes.values(
            'member__id',
            'member__first_name',
            'member__last_name'
        ).annotate(
            total_amount=Sum('amount'),
            tithe_count=Count('id')
        ).order_by('-total_amount')

        # 3. Monthly Breakdown (if no month filter)
        monthly_data = []
        if not month:
            monthly_data = tithes.dates('date_given', 'month').annotate(
                month_total=Sum('amount'),
                month_members=Count('member', distinct=True)
            )

        # 4. Available periods for dropdowns
        available_periods = Tithe.objects.dates('date_given', 'month')

        # Prepare response
        response_data = {
            "filters": {
                "year": year,
                "month": month
            },
            "summary": {
                "total_amount": float(total_summary['total_amount'] or 0),
                "member_count": total_summary['member_count']
            },
            "by_member": [
                {
                    "member_id": m['member__id'],
                    "member_name": f"{m['member__first_name']} {m['member__last_name']}",
                    "total_amount": float(m['total_amount']),
                    "tithe_count": m['tithe_count']
                } for m in by_member
            ],
            "monthly_trends": [
                {
                    "year": d.year,
                    "month": d.month,
                    "total_amount": float(d.month_total),
                    "member_count": d.month_members
                } for d in monthly_data
            ] if not month else [],
            "available_periods": [
                {"year": d.year, "month": d.month} for d in available_periods
            ]
        }

        return Response({
            "status": "success",
            "data": response_data
        })