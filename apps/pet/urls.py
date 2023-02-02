from django.urls import path

from apps.pet.views import CreatePetView, success_create_pet


urlpatterns = [
    path('crear', CreatePetView.as_view(), name = 'create_pet'),
    path('crear/correcto', success_create_pet, name = 'success_create_pet'),
]