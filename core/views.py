import random

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from services.models import Service

from .forms import CustomUserCreationForm
from .models import User


def home(request):
    services = Service.objects.filter(is_active=True).select_related("category")[:6]
    masters = User.objects.filter(user_type="master", is_active=True)
    return render(request, "home.html", {"services": services, "masters": masters})


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            code = str(random.randint(100000, 999999))
            user.verification_code = code
            user.save()

            send_mail(
                "Код подтверждения",
                f"Ваш код подтверждения: {code}",
                None,
                [user.email],
            )

            request.session["verify_user_id"] = user.id
            request.session["dev_verification_code"] = code
            messages.info(
                request,
                "Аккаунт создан. Введите код подтверждения на следующей странице.",
            )
            return redirect("verify")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})


def verify_view(request):
    dev_code = None
    from django.conf import settings

    if settings.DEBUG:
        dev_code = request.session.get("dev_verification_code")
        if not dev_code:
            user_id = request.session.get("verify_user_id")
            if user_id:
                user = User.objects.filter(id=user_id).first()
                if user:
                    dev_code = user.verification_code

    if request.method == "POST":
        code = request.POST.get("code")
        user_id = request.session.get("verify_user_id")
        if user_id:
            user = User.objects.get(id=user_id)
            if user.verification_code == code:
                user.is_active = True
                user.is_verified = True
                user.verification_code = None
                user.save()
                request.session.pop("verify_user_id", None)
                request.session.pop("dev_verification_code", None)
                messages.success(request, "Почта подтверждена. Войдите в аккаунт.")
                return redirect("login")
            messages.error(request, "Неверный код подтверждения.")
        else:
            messages.error(request, "Сессия истекла. Зарегистрируйтесь снова.")
    return render(request, "verify.html", {"dev_code": dev_code})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.user_type == "master":
                return redirect("master_dashboard")
            return redirect("home")

        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user and user.check_password(password) and not user.is_active:
            request.session["verify_user_id"] = user.id
            messages.warning(
                request,
                "Аккаунт не подтверждён. Введите код на странице подтверждения.",
            )
            return redirect("verify")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("home")
