import os
import datetime

from django.conf import settings
from django.core.exceptions import ValidationError

def validate_image_size(value):
    # Comprueba el tamaño de la imagen en bytes
    if value.size > 2*1024*1024: # Tamaño máximo 2 Mb
        raise ValidationError('El tamaño de la imagen no puede ser superior a 2 Mb')

def validate_image_format(value):
    # Comprueba el formato de la imagen
    format = value.name.split('.')[-1]
    
    # Si el formato no es 'jpg', 'jpeg' o 'png', lanza una excepción de validación
    if format not in ['jpg', 'jpeg', 'png']:
        raise ValidationError('Solo se permiten imágenes en formato jpg, jpeg o png')

def generate_path_upload_images(instance, image_name):
    # Recupera el nombre de usuario del objeto
    username = instance.username
    # Recupera el nombre base del archivo y la extención
    base_name, extension = image_name.split('.')
    # Genera el nuevo nombre y le asigna la extensión
    new_name = f'{username}.{extension}'
    # Genera la ruta completa del archivo
    path_fullname = os.path.join(settings.MEDIA_ROOT, "profile", username, new_name)
    # Si la ruta existe la borra
    if os.path.exists(path_fullname):
        os.remove(path_fullname)
    return os.path.join("profile", username, new_name)