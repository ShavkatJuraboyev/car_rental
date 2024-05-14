from django.urls import path
from dashboard.views import (
    dashboard, logIn, logOut,
    admins, admins_edit, admins_input, create_admin,
    admin_profile_view
)


urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('auth/login', logIn, name="login"),
    path('logout', logOut, name="logout"),
    path('admins/input/', admins_input, name="admins_input"),
    path('admin/<int:pk>/edit', admins_edit, name='admins_edit'),
    path('admins/', admins, name="admins"),
    path('create_admin/', create_admin, name='create_admin'),
    path('admin/profile/', admin_profile_view, name='admin_profile'),
]