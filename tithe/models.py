import datetime;
from django.db import models
from member.models import Member
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class TitheQuerySet(models.QuerySet):
    def by_year_month(self, year=None, month=None):
        queryset = self
        if year:
            queryset = queryset.filter(date_given__year=year)
        if month:
            queryset = queryset.filter(date_given__month=month)
        return queryset



class Tithe(models.Model):
    
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('check', 'Check'),
        ('card', 'Credit/Debit Card'),
        ('bank', 'Bank Transfer'),
        ('mobile', 'Mobile Money'),
    ]

    CONTRIBUTION_TYPES = [
        ('tithe', 'Tithe'),
        ('offering', 'Offering'),
        ('donation', 'Donation'),
        ('building', 'Building Fund'),
        ('mission', 'Missions'),
        ('other', 'Other'),

    ]

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name='tithes',
        verbose_name='Member'
    )

    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    date_given = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
    contribution_type = models.CharField(max_length=20, choices=CONTRIBUTION_TYPES, default='tithe')
    reference = models.CharField(max_length=100, blank=True)
    recorded_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='recorded_tithes',
        editable=False
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-date_given']
        verbose_name = "Tithe Record"
        verbose_name_plural = "Tithe Records"

    def __str__(self):
        return f"{self.member.member_no} - {self.member.full_name} - GHS{self.amount}"
    
    def save(self, *args, **kwargs):
        if not self.pk and not hasattr(self, 'recorded_by'):
            self.recorded_by = self._get_default_recorder()
        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        """Soft delete implementation"""
        self.is_deleted = True
        self.deleted_at = datetime.datetime.now();
        self.save()

    def _get_default_recorder(self):
        from django.contrib.auth import get_user_model
        return get_user_model().objects.filter(is_staff=True).first()
    
objects = TitheQuerySet.as_manager()  # Add custom manager