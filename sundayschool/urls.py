from django.urls import path,include
from rest_framework import routers
from sundayschool.views import SundaySchoolViewSet

# router = routers.DefaultRouter()
router = routers.SimpleRouter()
router.register(r'', SundaySchoolViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('birthdays_today', SundaySchoolViewSet.as_view({'get':'birthdays_today'}), name='sundayschool-birthdays-today'),
]