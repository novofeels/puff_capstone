from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from puffapi.models import *
from puffapi.views import *

router = routers.DefaultRouter(trailing_slash=False)
router = routers.DefaultRouter(trailing_slash=False)
router.register(r"users", Users, "user")


urlpatterns = [
    path("", include(router.urls)),
    path("register", register_user),
    path("login", login_user),
    path("api-token-auth", obtain_auth_token),
    path("api-auth", include("rest_framework.urls", namespace="rest_framework")),
    path("submit-score/", SubmitScoreView.as_view(), name="submit_score"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
