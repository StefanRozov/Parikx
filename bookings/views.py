from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from core.models import User
from services.models import Service

from .forms import BookingForm, BookingStatusForm
from .models import Booking


def master_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.user_type != "master":
            messages.error(request, "Доступ только для мастеров.")
            return redirect("home")
        return view_func(request, *args, **kwargs)

    return wrapper


@login_required
def booking_create(request, service_id):
    service = get_object_or_404(Service, pk=service_id, is_active=True)
    masters = User.objects.filter(user_type="master", is_active=True)

    if not masters.exists():
        messages.warning(request, "Сейчас нет доступных мастеров для записи.")
        return redirect("services_list")

    if request.method == "POST":
        form = BookingForm(request.POST, service=service)
        if form.is_valid():
            form.save(client=request.user, service=service)
            messages.success(request, "Вы успешно записались!")
            return redirect("booking_list")
    else:
        form = BookingForm(service=service)

    return render(
        request,
        "bookings/create.html",
        {"form": form, "service": service},
    )


@login_required
def booking_list(request):
    bookings = (
        Booking.objects.filter(client=request.user)
        .select_related("service", "master", "status")
        .order_by("-date")
    )
    return render(request, "bookings/list.html", {"bookings": bookings})


@login_required
def booking_cancel(request, pk):
    booking = get_object_or_404(Booking, pk=pk, client=request.user)
    if booking.status.name in ("Записан", "Подтверждён"):
        from .models import BookingStatus

        booking.status = BookingStatus.objects.get(name="Отменён")
        booking.save()
        messages.success(request, "Запись отменена.")
    else:
        messages.error(request, "Эту запись нельзя отменить.")
    return redirect("booking_list")


@login_required
@master_required
def master_dashboard(request):
    bookings = (
        Booking.objects.filter(master=request.user)
        .select_related("client", "service", "status")
        .order_by("date")
    )
    return render(request, "bookings/master_dashboard.html", {"bookings": bookings})


@login_required
@master_required
def master_update_status(request, pk):
    booking = get_object_or_404(Booking, pk=pk, master=request.user)

    if request.method == "POST":
        form = BookingStatusForm(request.POST)
        if form.is_valid():
            booking.status = form.cleaned_data["status"]
            booking.save()
            messages.success(request, "Статус записи обновлён.")
            return redirect("master_dashboard")
    else:
        form = BookingStatusForm()

    return render(
        request,
        "bookings/master_update.html",
        {"form": form, "booking": booking},
    )
