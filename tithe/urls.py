from django.urls import path, include
from rest_framework import routers
from tithe.views import TitheAnalyticsView, TitheViewSet

router = routers.SimpleRouter()
router.register(r'', TitheViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('analytics/', TitheAnalyticsView.as_view(), name='tithe-analytics'),
]