from django.shortcuts import render
from django.views.generic import CreateView

from apps.pet.forms import PetForm

# Create your views here.

class CreatePetView(CreateView):
    template_name = 'pet/create_pet.html'
    form_class = PetForm