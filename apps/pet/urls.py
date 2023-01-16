from django.urls import path

from apps.pet.views import CreatePetView


urlpatterns = [
    path('create', CreatePetView.as_view(), name = 'create_pet'),
]