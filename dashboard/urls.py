from django.urls import path
from dashboard.views import (
    dashboard, logIn, logOut,
    admins, admins_edit, admins_input, create_admin,
    admin_profile_view, car_input, cars, cars_edit,
    carmodels_input, carbreand_input, caryear_input, carprice_input,
    manzil_input, car_delete, admin_delete,
    full_appl, new_appl, conf_appl, retu_appl, refuse_appl,
    edit_appl
)


urlpatterns = [
    path('dashboard/', dashboard, name="dashboard"),
    path('auth/login', logIn, name="login"),
    path('logout', logOut, name="logout"),
    path('admins/input/', admins_input, name="admins_input"),
    path('admin/<int:pk>/edit', admins_edit, name='admins_edit'),
    path('admins/', admins, name="admins"),
    path('create_admin/', create_admin, name='create_admin'),
    path('', admin_profile_view, name='admin_profile'),

    path('car/input/', car_input, name='car_input'),
    path('car/<int:pk>/edit', cars_edit, name='cars_edit'),
    path('cars/', cars, name='cars'),
    path('carmodels/input/', carmodels_input, name='carmodels_input'),
    path('carbreand/input/', carbreand_input, name='carbreand_input'),
    path('caryear/input/', caryear_input, name='caryear_input'),
    path('carprice/input/', carprice_input, name='carprice_input'),
    path('manzil/input/', manzil_input, name='manzil_input'),
    path('car/<int:pk>/delete/', car_delete, name='car_delete'),
    path('admin/<int:pk>/delete/', admin_delete, name='admin_delete'),

    path("full/applicatins/", full_appl, name="full_appl"),
    path("new/applicatins/", new_appl, name="new_appl"),
    path("confirmed/applicatins/", conf_appl, name="conf_appl"),
    path("return/applicatins/", retu_appl, name="retu_appl"),
    path("refuse/applicatins/", refuse_appl, name="refuse_appl"),

    path('application/<int:pk>/edit', edit_appl, name='edit_appl'),
]