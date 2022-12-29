import uuid

from django.db import models

from apps.user.models import AbstractBaseModel
from apps.pet.validations import validate_image_format, validate_image_size, validate_phone, generate_path_upload_images

# Create your models here.

class Pet(AbstractBaseModel):
    SEX_CHOICES = [
        ('M', 'Male'), 
        ('F', 'Female')
    ]
    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large')
    ]
    TYPE_OF_PET_CHOICES = [
        ('D', 'Dog'),
        ('C', 'Cat')
    ]
    
    uuid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length = 100)
    breed = models.CharField(max_length = 100)
    age = models.PositiveIntegerField()
    sex = models.CharField(max_length = 1, choices = SEX_CHOICES)
    size = models.CharField(max_length = 2, choices = SIZE_CHOICES)
    type_of_pet = models.CharField(max_length = 1, choices = TYPE_OF_PET_CHOICES)
    description = models.TextField()
    
    def __str__(self):
        return self.name

class PetImage(AbstractBaseModel):
    uuid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    pet = models.ForeignKey(Pet, on_delete = models.CASCADE)
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

