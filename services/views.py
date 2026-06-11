from django.shortcuts import get_object_or_404, render

from .models import Service, ServiceCategory


def services_list(request):
    categories = ServiceCategory.objects.prefetch_related("service_set").all()
    active_services = Service.objects.filter(is_active=True).select_related("category")
    return render(
        request,
        "services/list.html",
        {"categories": categories, "services": active_services},
    )


def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk, is_active=True)
    return render(request, "services/detail.html", {"service": service})
