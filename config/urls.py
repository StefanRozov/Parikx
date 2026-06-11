from django.contrib import admin
from django.urls import include, path

from core.views import home, login_view, logout_view, register_view, verify_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("register/", register_view, name="register"),
    path("verify/", verify_view, name="verify"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("services/", include("services.urls")),
    path("bookings/", include("bookings.urls")),
]
