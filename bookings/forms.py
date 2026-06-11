import datetime

from django import forms
from django.utils import timezone

from core.models import User
from services.models import Service

from .models import Booking, BookingStatus


class BookingForm(forms.ModelForm):
    date = forms.DateField(
        label="Дата",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )
    time = forms.TimeField(
        label="Время",
        widget=forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
    )

    class Meta:
        model = Booking
        fields = ("master",)
        labels = {"master": "Мастер"}
        widgets = {"master": forms.Select(attrs={"class": "form-select"})}

    def __init__(self, *args, service=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = service
        self.fields["master"].queryset = User.objects.filter(
            user_type="master", is_active=True
        )
        self.fields["master"].empty_label = "Выберите мастера"

    def clean(self):
        cleaned = super().clean()
        date = cleaned.get("date")
        time = cleaned.get("time")
        master = cleaned.get("master")

        if date and time:
            booking_dt = timezone.make_aware(
                datetime.datetime.combine(date, time),
                timezone.get_current_timezone(),
            )
            if booking_dt <= timezone.now():
                raise forms.ValidationError("Нельзя записаться на прошедшее время.")
            cleaned["booking_datetime"] = booking_dt

        if master and date and time and self.service:
            booking_dt = cleaned["booking_datetime"]
            conflict = Booking.objects.filter(
                master=master,
                date=booking_dt,
                status__name__in=["Записан", "Подтверждён"],
            ).exists()
            if conflict:
                raise forms.ValidationError(
                    "У выбранного мастера это время уже занято."
                )

        return cleaned

    def save(self, client, service, commit=True):
        instance = super().save(commit=False)
        instance.client = client
        instance.service = service
        instance.date = self.cleaned_data["booking_datetime"]
        instance.status = BookingStatus.objects.get(name="Записан")
        if commit:
            instance.save()
        return instance


class BookingStatusForm(forms.Form):
    status = forms.ModelChoiceField(
        queryset=BookingStatus.objects.exclude(name="Записан"),
        label="Новый статус",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
