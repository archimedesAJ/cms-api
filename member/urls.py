from django.urls import path,include
from rest_framework import routers
from member.views import MemberViewSet

# router = routers.DefaultRouter()
router = routers.SimpleRouter()
router.register(r'', MemberViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('birthdays_today', MemberViewSet.as_view({'get':'birthdays_today'}), name='members-birthdays-today'),
]
