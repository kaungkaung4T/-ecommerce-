from django.shortcuts import render, redirect
from laptop.models import Laptop
from laptop.form import UploadForm
from django.contrib import messages
from laptop.models import Order
from laptop.models import item
import stripe
from django.contrib.auth.models import User
from django.contrib import messages
from django.core import exceptions
from django.http import JsonResponse, HttpResponse
from laptop.models import Category
from display.models import Profile

# Create your views here.
def home(request):
    l = Laptop.objects.all()
    l2 = Laptop.objects.all()
    c = Category.objects.all()

    return render(request, "index.html",
                  {"l":l, "l2":l2, "c": c})

def search(request):
    if request.method == "POST":
        s = request.POST["search"]
        if Laptop.objects.filter(title__icontains=s).exists():
            laptop = Laptop.objects.filter(title__icontains=s)
            return render(request, "search.html",
                        {"s":s, "laptop":laptop})
        else:
            nothing = "did not match any documents."
            return render(request, "search.html",
                        {"se":s, "nothing":nothing})
    else:
        return render(request, "search.html")

def category(request, pk):

    if Laptop.objects.filter(title__icontains=pk).exists():
        laptop = Laptop.objects.filter(title__icontains=pk)
        return render(request, "category.html",
                    {"laptop":laptop, "pk":pk})
    else:
        nothing = "No Users' products here."
        return render(request, "category.html",
                      {"nothing":nothing, "pk":pk})


def profile(request):
    l = Laptop.objects.filter(user__username=request.user)

    return render(request, "profile.html",
                  {"laptop": l})


def upload(request):
    if request.method == "POST":
        if User.objects.filter(username=request.user).exists():
            lu = UploadForm(request.POST, request.FILES)
            if lu.is_valid():
                instance = lu.save(commit=False)
                instance.user = request.user
                instance.save()
                messages.success(request, "Upload Success")
                return redirect(f"view/{instance.id}")
        else:
            messages.info(request, "Please sign in to sell a product")
            return redirect("upload")
    else:
        lu = UploadForm()

    return render(request, "upload.html",
                  {"lu":lu})

def update(request, pk):
    if request.method == "POST":
        l = Laptop.objects.get(id=pk)
        u = UploadForm(request.POST, request.FILES, instance=l)
        if u.is_valid():
            u.save()
            messages.success(request, "Product was updated ")
            return redirect(f"/view/{l.id}")
    else:
        l = Laptop.objects.get(id=pk)
        u = UploadForm(instance=l)

    return render(request, "update.html",
                  {"u":u, "l":l})


def delete(request, pk):
    if request.method == "POST":
        l = Laptop.objects.get(id=pk)
        l.delete()
        messages.success(request, "Product was deleted")
        return redirect("profile")

def order(request, pk):
    if request.method == "POST":
        # p = Profile.objects.get(id=request.user.id)
        # p.is_verified = True
        # p.save()

        if User.objects.filter(username=request.user).exists():
            if Order.objects.filter(user=request.user).exists():
                oo = Order.objects.get(user=request.user)
                count = len(oo.newitem.all())+1
                if item.objects.filter(items_id=pk).exists():
                    i = item.objects.get(user=request.user, items_id=pk)
                    oo.newitem.add(i)
                    return HttpResponse("Your order was already added!")
                else:
                    get, created = item.objects.get_or_create(user=request.user, items_id=pk, number=count)
                    oo.newitem.add(get)
                    return HttpResponse("Your order added, please check order lists.")

            else:
                get, created = item.objects.get_or_create(user=request.user, items_id=pk)

            if Order.objects.filter(user=request.user).exists():
                o = Order.objects.get(user=request.user)
            else:
                o = Order.objects.create(user=request.user)
                o.save()
            o.newitem.add(get)

            return HttpResponse("Your order added, please check order lists.")
        else:
            return redirect("orderlist")

def order2(request):
    if User.objects.filter(username=request.user).exists():
        if Order.objects.filter(user=request.user).exists():
            o = Order.objects.get(user=request.user)
        else:
            o = Order.objects.all()
        return render(request, "orderlist.html", {"o": o})
    else:
        return render(request, "orderlist.html")


def order_payment(request):
    if request.method == "POST":
        if Order.objects.filter(user=request.user).exists() and item.objects.filter(user=request.user).exists():
            i = item.objects.filter(user=request.user)
            o = Order.objects.get(user=request.user)
            container = []
            count = 0
            for mechanism in o.newitem.all():
                count += 1

                if mechanism.items.discount:
                    main = {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': mechanism.items.title,
                            },
                            'unit_amount_decimal': mechanism.items.discount * 100,
                        },
                        'quantity': 1,
                    }
                    container.append(main)
                else:
                    main = {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': mechanism.items.title,
                            },
                            'unit_amount_decimal': mechanism.items.price * 100,
                        },
                        'quantity': 1,
                    }
                    container.append(main)

            stripe.api_key = "sk_test_51KrzHwJK74gmekDIJINKA2hs67jIgHJheBvdWzyZITKa3rRP2ZtewegJy6Wd5toCkZl1J36oZCcYG4liIfrWRBre00SN3J9Brr"
            session = stripe.checkout.Session.create(
                line_items=
                    container
                ,
                mode='payment',
                success_url= "http://127.0.0.1:8000/",
                cancel_url= "http://127.0.0.1:8000/",
            )
            o.delete()
            i.delete()

            return redirect(session.url, code=303)
        else:
            messages.info(request, "No order product")
            return redirect("orderlist")

def order_delete(request, pk):
    i = item.objects.get(id=pk)
    i.delete()
    return redirect("orderlist")


def buy(request, pk):
    l = Laptop.objects.get(id=pk)
    container = []
    if l.discount:
        main = {
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': l.title,
                },
                'unit_amount_decimal': l.discount * 100,
            },
            'quantity': 1,
        }
        container.append(main)
    else:
        main = {
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': l.title,
                },
                'unit_amount_decimal': l.price * 100,
            },
            'quantity': 1,
        }
        container.append(main)

    stripe.api_key = "sk_test_51KrzHwJK74gmekDIJINKA2hs67jIgHJheBvdWzyZITKa3rRP2ZtewegJy6Wd5toCkZl1J36oZCcYG4liIfrWRBre00SN3J9Brr"
    session = stripe.checkout.Session.create(
        line_items=
            container
        ,
        mode='payment',
        success_url="http://127.0.0.1:8000/",
        cancel_url="http://127.0.0.1:8000/",
    )

    return redirect(session.url, code=303)


def view(request, pk):
    laptop = Laptop.objects.get(id=pk)

    return render(request, "view.html",
                  {"laptop":laptop})