from django.contrib import admin

from apps.pet.models import Pet, PetImage, AdoptionForm, AdoptionRequest

# Register your models here.

admin.site.register(Pet)
admin.site.register(PetImage)
admin.site.register(AdoptionForm)
admin.site.register(AdoptionRequest)
