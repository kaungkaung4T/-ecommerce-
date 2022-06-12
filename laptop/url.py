from django.urls import path
from laptop import views


urlpatterns = [
    path("", views.home, name="index"),
    path("upload", views.upload, name="upload"),
    path("profile", views.profile, name="profile"),
    path("update/<str:pk>/", views.update, name="update"),
    path("delete/<str:pk>", views.delete, name="delete"),
    path("order/<str:pk>", views.order, name="order"),
    path("orderlist", views.order2, name="orderlist"),
    path("order_payment", views.order_payment, name="order_payment"),
    path("order_delete/<str:pk>", views.order_delete, name="order_delete"),
    path("search", views.search, name="search"),
    path("category/<str:pk>", views.category, name="category"),
    path("view/<str:pk>", views.view, name="view"),
    path("buy/<str:pk>", views.buy, name="buy"),
]

