from django import forms
from django.forms.widgets import Select

from apps.user.models import CustomUser
from apps.pet.models import Pet, AdoptionForm

class PetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        self.fields['name'].label = 'Nombre'
        self.fields['name'].widget.attrs['placeholder'] = 'example'
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['aria-describedby'] = 'nameHelp'
        
        self.fields['breed'].label = 'Raza'
        self.fields['breed'].widget.attrs['placeholder'] = 'Raza'
        self.fields['breed'].widget.attrs['class'] = 'form-control'
        self.fields['breed'].widget.attrs['autocomplete'] = 'off'
        self.fields['breed'].widget.attrs['aria-describedby'] = 'breedHelp'
        
        self.fields['age'].label = 'Edad'
        self.fields['age'].widget.attrs['placeholder'] = '0'
        self.fields['age'].widget.attrs['class'] = 'form-control'
        self.fields['age'].widget.attrs['aria-describedby'] = 'ageHelp'
        
        self.fields['sex'].label = 'Género'
        self.fields['sex'].widget.attrs['class'] = 'custom-select'
        self.fields['sex'].widget.attrs['aria-describedby'] = 'sexHelp'
        
        self.fields['size'].label = 'Tamaño'
        self.fields['size'].widget.attrs['class'] = 'custom-select'
        self.fields['size'].widget.attrs['aria-describedby'] = 'sizeHelp'
        
        self.fields['type_of_pet'].label = 'Tipo de mascota'
        self.fields['type_of_pet'].widget.attrs['class'] = 'custom-select'
        self.fields['type_of_pet'].widget.attrs['aria-describedby'] = 'type_of_petHelp'
        
        self.fields['description'].label = 'Descripción'
        self.fields['description'].widget.attrs['placeholder'] = 'Escribe una pequeña descripción a cerca de la mascota!'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['autocomplete'] = 'off'
        self.fields['description'].widget.attrs['aria-describedby'] = 'descriptionHelp'
        
        queryset = CustomUser.objects.all()
        self.fields['created_by'] = forms.ModelChoiceField(queryset = queryset, widget = forms.HiddenInput(), initial = user)
        
        self.fields['modified_by'] = forms.ModelChoiceField(queryset = queryset, widget = forms.HiddenInput(), initial = user)
        
    class Meta:
        model = Pet
        fields = [
            'created_by',
            'modified_by',
            'name',
            'breed',
            'age',
            'sex',
            'size',
            'type_of_pet',
            'description'
        ]


class ImageForm(forms.Form):
    images = forms.ImageField(
            widget = forms.ClearableFileInput(
                attrs = {
                    'multiple':True, 
                    'required':True,
                    'max_upload_num':5,
                    'class':'upload__inputfile',
                    'accept':'.jpg, .jpeg, .png',
                    'data-max_length':'5'
                }
            ),
            label='Imágenes'
        )
    
    def clean_images(self):
        images = self.cleaned_data.get('images')
        if len(images) > 5:
            raise forms.ValidationError("Solo puedes subir un máximo de 5 imagenes")
        return images


class AdoptionFormF(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        self.fields['name'].label = 'Nombre'
        self.fields['name'].widget.attrs['placeholder'] = 'nombre'
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['aria-describedby'] = 'nameHelp'
        
        self.fields['last_name'].label = 'Apellido'
        self.fields['last_name'].widget.attrs['placeholder'] = 'apellido'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['autocomplete'] = 'off'
        self.fields['last_name'].widget.attrs['aria-describedby'] = 'lastNameHelp'
        
        self.fields['second_last_name'].label = 'Segundo apellido'
        self.fields['second_last_name'].widget.attrs['placeholder'] = 'segundo apellido'
        self.fields['second_last_name'].widget.attrs['class'] = 'form-control'
        self.fields['second_last_name'].widget.attrs['autocomplete'] = 'off'
        self.fields['second_last_name'].widget.attrs['aria-describedby'] = 'secondLastNameHelp'
        
        self.fields['email'].label = 'Correo electrónico'
        self.fields['email'].widget.attrs['placeholder'] = 'email@example.com'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['autocomplete'] = 'off'
        self.fields['email'].widget.attrs['aria-describedby'] = 'emailHelp'
        
        self.fields['phone_number'].label = 'Número de teléfono'
        self.fields['phone_number'].widget = forms.TextInput(attrs = {
                'type':'number',
                'placeholder': '+55 5555 5555',
                'class': 'form-control',
                'autocomplete': 'off',
                'aria-describedby': 'phone_numberHelp',
                'pattern': '/^(\+?52)(1|01)?[0-9]{2,3}\d{8}$/'
            }
        )
        
        self.fields['address'].label = 'Calle y número'
        self.fields['address'].widget.attrs['placeholder'] = 'calle y número'
        self.fields['address'].widget.attrs['class'] = 'form-control'
        self.fields['address'].widget.attrs['autocomplete'] = 'off'
        self.fields['address'].widget.attrs['aria-describedby'] = 'addressHelp'
        
        self.fields['postal_code'].label = 'Código postal'
        self.fields['postal_code'].widget.attrs['placeholder'] = 'código postal'
        self.fields['postal_code'].widget.attrs['class'] = 'form-control'
        self.fields['postal_code'].widget.attrs['autocomplete'] = 'off'
        self.fields['postal_code'].widget.attrs['max_length'] = 5
        self.fields['postal_code'].widget.attrs['aria-describedby'] = 'postal_codeHelp'
        
        self.fields['country'].label = 'País'
        self.fields['country'].widget.attrs['placeholder'] = 'País de residencia'
        self.fields['country'].widget.attrs['class'] = 'form-control'
        self.fields['country'].widget.attrs['autocomplete'] = 'off'
        self.fields['country'].widget.attrs['aria-describedby'] = 'countryHelp'
        self.fields['country'].widget.attrs['readonly'] = True
        
        self.fields['state'].label = 'Estado'
        self.fields['state'].widget.attrs['placeholder'] = 'Estado'
        self.fields['state'].widget.attrs['class'] = 'form-control'
        self.fields['state'].widget.attrs['autocomplete'] = 'off'
        self.fields['state'].widget.attrs['aria-describedby'] = 'stateHelp'
        self.fields['state'].widget.attrs['readonly'] = True
        
        self.fields['city'].label = 'Ciudad'
        self.fields['city'].widget.attrs['placeholder'] = 'Ciudad'
        self.fields['city'].widget.attrs['class'] = 'form-control'
        self.fields['city'].widget.attrs['autocomplete'] = 'off'
        self.fields['city'].widget.attrs['aria-describedby'] = 'cityHelp'
        self.fields['city'].widget.attrs['readonly'] = True
        
        town_choices = [(town, town) for town in self.fields['town'].widget.attrs.get('choices', [])]
        self.fields['town'].label = 'Delegación, municipio o Alcaldía'
        self.fields['town'].widget = Select(choices = town_choices, attrs ={
            'placeholder': 'Delegación - Municipio o Alcaldía',
            'class': 'form-control',
            'autocomplete': 'off',
            'aria-describedby': 'townHelp'
        })
        
        self.fields['message'].label = 'Mensaje'
        self.fields['message'].widget.attrs['placeholder'] = 'Escribe un pequeño mensaje de porqué quieres adoptar esta mascota y como quieres que te contactemos!'
        self.fields['message'].widget.attrs['class'] = 'form-control'
        self.fields['message'].widget.attrs['autocomplete'] = 'off'
        self.fields['message'].widget.attrs['aria-describedby'] = 'messageHelp'
        
        queryset = CustomUser.objects.all()
        self.fields['created_by'] = forms.ModelChoiceField(queryset = queryset, widget = forms.HiddenInput(), initial = user)
        
        self.fields['modified_by'] = forms.ModelChoiceField(queryset = queryset, widget = forms.HiddenInput(), initial = user)
    
    class Meta:
        model = AdoptionForm
        fields = [
            'created_by',
            'modified_by',
            'name',
            'last_name',
            'second_last_name',
            'email',
            'phone_number',
            'postal_code',
            'address',
            'country',
            'state',
            'city',
            'town',
            'message'
        ]