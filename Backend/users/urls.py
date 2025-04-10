from django.urls import path
from .views import ProfileDescription
from rest_framework.routers import DefaultRouter
from .viewsets import UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = router.urls
