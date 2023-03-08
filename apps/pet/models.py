import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.user.models import AbstractBaseModel
from apps.pet.validations import validate_image_format, validate_image_size, validate_phone, generate_path_upload_images

# Create your models here.

class Pet(AbstractBaseModel):
    SEX_CHOICES = [
        ('M', _('Macho')), 
        ('F', _('Hembra'))
    ]
    SIZE_CHOICES = [
        ('XS', _('Extra Pequeño')),
        ('S', _('Pequeño')),
        ('M', _('Mediano')),
        ('L', _('Grande')),
        ('XL', _('Extra Grande'))
    ]
    TYPE_OF_PET_CHOICES = [
        ('D', _('Perro')),
        ('C', _('Gato'))
    ]
    
    uuid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length = 100)
    breed = models.CharField(max_length = 100)
    age = models.PositiveIntegerField()
    sex = models.CharField(max_length = 1, choices = SEX_CHOICES)
    size = models.CharField(max_length = 2, choices = SIZE_CHOICES)
    type_of_pet = models.CharField(max_length = 1, choices = TYPE_OF_PET_CHOICES)
    description = models.TextField()
    status = models.BooleanField(default = True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Mascota"
        verbose_name_plural = "Mascotas"

class PetImage(AbstractBaseModel):
    uuid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    pet = models.ForeignKey(Pet, on_delete = models.CASCADE, related_name = 'pet_images')
    image = models.ImageField(upload_to = generate_path_upload_images,
                            null = True, 
                            blank = True,
                            validators = [
                                validate_image_size, 
                                validate_image_format
                            ]
                        )
    
    def __str__(self):
        return f'image {self.pet.name}'
    
    def save(self, *args, **kwargs):
        # Si el objeto ya existe en la base de datos, recupera la imagen anterior
        if self.pk and PetImage.objects.filter(pk = self.pk).exists():
            old_image = PetImage.objects.get(pk = self.pk).image
        else:
            old_image = None
            
        super(PetImage, self).save(*args, **kwargs)
        
        # Si la imagen anterior es diferente a la imagen actual y existe, elimina la imagen anterior
        if old_image and old_image != self.image:
            old_image.storage.delete(old_image.name)
    
    class Meta:
        verbose_name = "Imagen"
        verbose_name_plural = "Imagenes"

class AdoptionForm(AbstractBaseModel):
    uuid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    second_last_name = models.CharField(max_length = 100, null = True, blank = True)
    email = models.EmailField()
    phone_number = models.CharField(validators = [validate_phone], max_length = 12)
    country = models.CharField(max_length = 100, default = "México")
    city = models.CharField(max_length = 100)
    state = models.CharField(max_length = 100)
    town = models.CharField(max_length = 100)
    postal_code = models.CharField(max_length = 5)
    address = models.CharField(max_length = 250)
    message = models.TextField()

    def __str__(self):
        return f'Formulario de: {self.name}'
    
    class Meta:
        verbose_name = "Formulario de adopción"
        verbose_name_plural = "Formularios de adopción"
        
        
class AdoptionRequest(AbstractBaseModel):
    STATUS_CHOICES = [
        ('S', _('Enviado')),
        ('A', _('Aprobado')),
        ('R', _('Rechazado'))
    ]
    uuid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    pet = models.ForeignKey(Pet, on_delete = models.CASCADE, related_name = 'pet_adoption_requests')
    adoption_form = models.ForeignKey(AdoptionForm, on_delete = models.CASCADE, related_name = 'form_adoption_requests')
    status = models.CharField(max_length = 1, choices = STATUS_CHOICES)
    
    def __str__(self):
        return f'Solicitud de adopción para: {self.pet.name}'

    class Meta:
        verbose_name = "Solicitud de adopción"
        verbose_name_plural = "Solcitudes de adopción"