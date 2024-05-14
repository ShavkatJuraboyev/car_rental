from django.urls import path
from carrental.views import (
    home, about, pricing, car, blog, contact, 
    car_single, blog_single, RegisterView, 
    login_user, logout_user, checkout, confirmation
    )
urlpatterns = [
    path('', home, name="home"),
    path('about/', about, name="about"),
    path('pricing/', pricing, name="pricing"),
    path('car/', car, name="car"),
    path('blog/', blog, name="blog"),
    path('contact/', contact, name="contact"),
    path('car_single/<int:pk>/', car_single, name="car_single"),
    path('blog_single/', blog_single, name="blog_single"),

    path('register/', RegisterView.as_view(), name="register"),
    path('login/', login_user, name="login"), 
    path('logout/', logout_user, name="logout"),
    path('checkout/<int:pk>/', checkout, name='checkout'),
    path('confirmation/', confirmation, name='confirmation'),
]