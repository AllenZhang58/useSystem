from django.urls import include, path

from usersInfo.views import loginTop

urlpatterns = [
    path('loginTop', loginTop, name='login-top'),
    path('loginSide', loginTop, name='login-side'),
]