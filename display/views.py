from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from laptop.models import Order
from laptop.models import item
import uuid
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
from display.utils import token_email
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from display.serializer import LaptopSerializer
from laptop.models import Laptop
# Create your views here.

class resting(APIView):
    serializer_class = LaptopSerializer

    def get(self, request):
        l = Laptop.objects.all()
        ls = LaptopSerializer(l, many=True)
        return Response(ls.data)

    def post(self, request):
        ls = LaptopSerializer(data=request.data)
        if ls.is_valid():
            ls.save()
            return Response(ls.data)

    def put(self, request, pk):
        l = Laptop.objects.get(id=pk)
        ls = LaptopSerializer(l, data=request.data)
        if ls.is_valid():
            ls.save()
            return Response(ls.data)
        return Response(ls.errors)

    def delete(self, request, pk):
        l = Laptop.objects.get(id=pk)
        l.delete()
        success = {}
        success["success"] = "success"
        return Response(data=success)

class resting2(APIView):
    serializer_class = LaptopSerializer

    def put(self, request, pk):
        l = Laptop.objects.get(id=pk)
        ls = LaptopSerializer(l, data=request.data)
        if ls.is_valid():
            ls.save()
            return Response(ls.data)
        return Response(ls.errors)

    def delete(self, request, pk):
        l = Laptop.objects.get(id=pk)
        l.delete()
        success = {}
        success["success"] = "success"
        return Response(data=success)


@api_view(["PUT"])
def update(request, pk):
    serializer_class = LaptopSerializer
    l = Laptop.objects.get(id=pk)
    ls = LaptopSerializer(l, data=request.data)
    if ls.is_valid():
        ls.save()
        return Response(ls.data)
    return Response(ls.errors)


@api_view(["DELETE"])
def delete(request, pk):
    l = Laptop.objects.get(id=pk)
    l.delete()
    success = {}
    success["success"] = "success"
    return Response(data=success)


def send_email(request, user):
    current = get_current_site(request)
    title = '雨点 account activation'
    body = render_to_string('email.html',
                            {"user":user,
                             "domain":current,
                             "user_id":urlsafe_base64_encode(force_bytes(user.id)),
                             "token":token_email.make_token(user),
                             })
    e = EmailMessage(subject=title, body=body, from_email=settings.EMAIL_HOST_USER, to=[user.email])
    e.send()
# kaungminkhant4t99@gmail.com

def home(request):
    return render(request, "index.html")


def registration(request):
    if request.method == "POST":
        name = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 == password2:
            if User.objects.filter(username=name).exists():
                messages.info(request, "Username already exist")
                return redirect("registration")

            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already exist")
                return redirect("registration")

            user = User.objects.create_user(username=name, email=email, password=password1)
            user.save()

            # email
            try:
                send_email(request, user)
            except Exception as e:
                messages.info(request, "Invalid Email")
                return redirect("registration")

            messages.success(request, "Account created, please verify your account in Email")
            return redirect("login")
        else:
            messages.info(request, "Passwords are not same")
            return redirect("registration")
    else:
        return render(request, "registration.html")

def login(request):
    if request.method == "POST":
        name = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=name, password=password)


        if user is not None:
            if user.profile.is_verified:
                auth.login(request, user)
                return redirect("/")
            else:
                messages.info(request, "Please verify your account in Email")
                return redirect("login")
        else:
            messages.info(request, "Counldn't find your username")
            login_error_mes = "You should check in on some of those fields."
            return render(request, "login.html",
                          {"login_error_mes":login_error_mes})
    else:
        return render(request, "login.html")

def logout(request):
    if item.objects.filter(user=request.user).exists:
        i = item.objects.filter(user=request.user)
        i.delete()
    if Order.objects.filter(user=request.user).exists:
        o = Order.objects.filter(user=request.user)
        o.delete()
    else:
        auth.logout(request)
        return redirect("/")

    auth.logout(request)
    return redirect("/")

def accept(request, user_id, token):
    try:
        uid = force_text(urlsafe_base64_decode(user_id))
        user = User.objects.get(id=uid)

    except Exception as e:
        user = None

    if user and token_email.check_token(user, token):
        user.profile.is_verified = True
        user.save()

        messages.success(request,"Account Created and Verified")
        return redirect("login")

    return redirect("login")
