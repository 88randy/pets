import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from apps.user.validations import validate_image_size, validate_image_format, generate_path_upload_images

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password = None, **extra_fields):
        if not username:
            raise ValueError('El nombre de usuario es obligatorio')
        if not email:
            raise ValueError('El email es obligatorio')
        user = self.model(username = username, email = self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    TYPE_USER = (
        ('P', 'Persona'),
        ('O', 'Organización'),
    )
    
    uuid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    username = models.CharField(max_length = 150, unique = True)
    email = models.EmailField(unique = True)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    type_user = models.CharField(max_length = 1, choices = TYPE_USER)
    profile_picture = models.ImageField(upload_to = generate_path_upload_images,
                                    null = True, 
                                    blank = True,
                                    validators = [
                                        validate_image_size, 
                                        validate_image_format
                                    ]
                                )
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Si el objeto ya existe en la base de datos, recupera la imagen anterior
        if self.pk and CustomUser.objects.filter(pk=self.pk).exists():
            old_profile_picture = CustomUser.objects.get(pk = self.pk).profile_picture
        else:
            old_profile_picture = None
            
        super(CustomUser, self).save(*args, **kwargs)
        
        # Si la imagen anterior es diferente a la imagen actual y existe, elimina la imagen anterior
        if old_profile_picture and old_profile_picture != self.profile_picture:
            old_profile_picture.storage.delete(old_profile_picture.name)
        
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
