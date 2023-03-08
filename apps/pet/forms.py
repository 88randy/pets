from django import forms

from apps.user.models import CustomUser
from apps.pet.models import Pet

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
        
        self.fields['created_by'] = forms.ModelChoiceField(queryset = CustomUser.objects.all(), widget = forms.HiddenInput(), initial = user)
        
        self.fields['modified_by'] = forms.ModelChoiceField(queryset = CustomUser.objects.all(), widget = forms.HiddenInput(), initial = user)
        
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