from django.urls import path

from apps.pet.views import *


urlpatterns = [
    path('crear', PetCreateView.as_view(), name = 'pet_create'),
    path('mis-mascotas', MyPetListView.as_view(), name = 'my_pet_list'),
    path('mascotas', ListOfPetsForAdoptionView.as_view(), name = 'list_of_pets_for_adoption'),
    path('detalle/<uuid:pk>', PetDetailView.as_view(), name = 'pet_detail'),
    path('adoptar/<uuid:pk>/', AdoptionFormView.as_view(), name = 'adoption_form'),
    path('crear/correcto', success_create_pet, name = 'success_create_pet'),
    path('postal-codes/<str:postal_code>/', get_postal_details, name='get_postal_details'),
]