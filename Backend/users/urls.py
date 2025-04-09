from django.urls import path
from .views import Register, Login, ProfileDescription, ProfileImage


urlpatterns = [
    path("register/", Register.as_view()),
    path("login/", Login.as_view()),
    path("profile/description/<int:pk>/", ProfileDescription.as_view()),
    path("profile/upload-img/<int:pk>/", ProfileImage.as_view()),
]
