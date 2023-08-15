from django.urls import path
from . import views

app_name="accounts"
urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('loginPage/',views.login_page,name='login_page'),
    path('login/',views.user_login,name='user_login'),
    path('logout/',views.user_logout,name='logout')
]