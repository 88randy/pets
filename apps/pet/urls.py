from django.urls import path

from apps.pet.views import *


urlpatterns = [
    path('crear', PetCreateView.as_view(), name = 'create_pet'),
    path('detalle/<uuid:pk>', PetDetail.as_view(), name = 'pet_detail'),
    path('crear/correcto', success_create_pet, name = 'success_create_pet'),
]