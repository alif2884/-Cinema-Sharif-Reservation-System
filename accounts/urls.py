from django.urls import path
from . import views
from .views import login_view, logout_view, signup_view, charge_wallet

urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('auth/', views.auth_entry, name='auth_entry'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
    path('charge-wallet/', charge_wallet, name='charge_wallet')
]