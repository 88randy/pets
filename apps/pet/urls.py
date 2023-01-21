from django.urls import path

from apps.pet.views import CreatePetView


urlpatterns = [
    path('crear', CreatePetView.as_view(), name = 'create_pet'),
]