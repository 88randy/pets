from django.urls import reverse
from django.db import transaction
from django.shortcuts import render
from django.views.generic import CreateView

from apps.pet.forms import PetForm, ImageForm
from apps.pet.models import PetImage

# Create your views here.

class CreatePetView(CreateView):
    template_name = 'pet/create_pet.html'
    form_class = PetForm
    success_url = '/mascota/crear/correcto'
    
    @transaction.atomic
    def form_valid(self, form):
        self.object = form.save()
        user = self.request.user
        image_list = self.request.FILES.getlist('images')
        for image in image_list:
            pet_image = PetImage(
                    created_by = user,
                    modified_by = user,
                    pet = self.object, 
                    image = image
                )
            pet_image.save()
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        if "form" not in kwargs:
            kwargs["form"] = self.get_form()
        kwargs["images_form"] = ImageForm
        return super().get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    """ def get_success_url(self):
        return reverse('pet_created', args=(self.object.pk,)) """

# Success forms

def success_create_pet(request):
    return render(request, 'pet\success_create_pet.html')