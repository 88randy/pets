from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.user.models import CustomUser

class CustomUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['username'].label = 'Nombre de usuario'
        self.fields['username'].widget.attrs['placeholder'] = 'example'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['autocomplete'] = 'off'
        self.fields['username'].widget.attrs['aria-describedby'] = 'usernameHelp'
        
        self.fields['email'].label = "Correo electrónico"
        self.fields['email'].widget.attrs['placeholder'] = 'email@example.com'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['autocomplete'] = 'off'
        self.fields['email'].widget.attrs['aria-describedby'] = 'emailHelp'
        
        self.fields['password1'].label = 'Contraseña'
        self.fields['password1'].widget = forms.PasswordInput()
        self.fields['password1'].widget.attrs['class'] = 'form-control password'
        self.fields['password1'].widget.attrs['placeholder'] = '******'
        self.fields['password1'].widget.attrs['aria-describedby'] = 'password1Help'
        
        self.fields['password2'].label = 'Repite la contraseña'
        self.fields['password2'].widget = forms.PasswordInput()
        self.fields['password2'].widget.attrs['class'] = 'form-control password'
        self.fields['password2'].widget.attrs['placeholder'] = '******'
        self.fields['password2'].widget.attrs['aria-describedby'] = 'password2Help'
        
        self.fields['type_user'].label = 'Tipo de usuario'
        self.fields['type_user'].widget.attrs['class'] = 'form-select'
        self.fields['type_user'].widget.attrs['aria-describedby'] = 'type_userHelp'
        
        self.fields['profile_picture'].label = 'Imagen de perfil'
        self.fields['profile_picture'].widget = forms.FileInput()
        self.fields['profile_picture'].widget.attrs['class'] = 'form-control'
        self.fields['profile_picture'].widget.attrs['onchange'] = 'previewImage(event);'
        self.fields['profile_picture'].widget.attrs['accept'] = 'image/jpg, image/jpeg, image/png'
        self.fields['profile_picture'].widget.attrs['aria-describedby'] = 'profile_pictureHelp'
        
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'password1', 
            'password2',
            'type_user',
            'profile_picture',
        ]