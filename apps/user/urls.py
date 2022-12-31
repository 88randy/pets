from django.urls import path

from apps.user.views import IndexView, SignupView

urlpatterns = [
    path('signup', SignupView.as_view(), name = 'signup'),
]