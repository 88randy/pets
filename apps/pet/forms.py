from django import forms

from apps.pet.models import Pet

class PetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['name'].label = 'Nombre'
        self.fields['name'].widget.attrs['placeholder'] = 'example'
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['aria-describedby'] = 'nameHelp'
        
        self.fields['breed'].label = 'Raza'
        self.fields['breed'].widget.attrs['placeholder'] = 'Completa si sabes la raza'
        self.fields['breed'].widget.attrs['class'] = 'form-control'
        self.fields['breed'].widget.attrs['autocomplete'] = 'off'
        self.fields['breed'].widget.attrs['aria-describedby'] = 'breedHelp'
        
        self.fields['age'].label = 'Edad'
        self.fields['age'].widget.attrs['placeholder'] = '0'
        self.fields['age'].widget.attrs['class'] = 'form-control'
        self.fields['age'].widget.attrs['aria-describedby'] = 'ageHelp'
        
        self.fields['sex'].label = 'Género'
        self.fields['sex'].widget.attrs['class'] = 'form-select'
        self.fields['sex'].widget.attrs['aria-describedby'] = 'sexHelp'
        
        self.fields['size'].label = 'Tamaño'
        self.fields['size'].widget.attrs['class'] = 'form-select'
        self.fields['size'].widget.attrs['aria-describedby'] = 'sizeHelp'
        
        self.fields['type_of_pet'].label = 'Tipo de mascota'
        self.fields['type_of_pet'].widget.attrs['class'] = 'form-select'
        self.fields['type_of_pet'].widget.attrs['aria-describedby'] = 'type_of_petHelp'
        
        self.fields['description'].label = 'Descripción'
        self.fields['description'].widget.attrs['placeholder'] = 'Escribe una pequeña descripción a cerca de la mascota!'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['autocomplete'] = 'off'
        self.fields['description'].widget.attrs['aria-describedby'] = 'descriptionHelp'

    class Meta:
        model = Pet
        fields = [
            'name',
            'breed',
            'age',
            'sex',
            'size',
            'type_of_pet',
            'description'
        ]