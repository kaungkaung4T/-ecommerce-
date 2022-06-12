from django.urls import path, include
from display import views

urlpatterns = [
    path("registration", views.registration, name="registration"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("accept/<str:user_id>/<str:token>", views.accept, name="accept"),

    path("rest", views.resting.as_view(), name="rest"),
    path("rest/update/<str:pk>", views.resting.as_view(), name="rest"),
    path("rest/delete/<str:pk>", views.resting.as_view(), name="rest"),

    path("rest2/update/<str:pk>", views.resting2.as_view(), name="update"),
    path("rest2/delete/<str:pk>", views.resting2.as_view(), name="delete"),

    path("update2/<str:pk>", views.update, name="update2"),
    path("delete2/<str:pk>", views.delete, name="delete2"),
    path("api-auth", include("rest_framework.urls"))
]

