from django.urls import path,include
from rest_framework import routers
from visitor.views import VisitorViewSet

router = routers.SimpleRouter()
router.register(r'', VisitorViewSet)


urlpatterns = [
    path('', include(router.urls)),
]