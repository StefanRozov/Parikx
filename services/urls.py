from django.urls import path

from .views import service_detail, services_list

urlpatterns = [
    path("", services_list, name="services_list"),
    path("<int:pk>/", service_detail, name="service_detail"),
]
