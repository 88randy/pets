from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from apps.user.forms import CustomUserForm

class IndexView(TemplateView):
    template_name = 'index.html'

class SignupView(FormView):
    template_name = 'user/signup.html'
    form_class = CustomUserForm
    success_url = reverse_lazy('index')
    
    def form_valid(self, form):
        # Procesa la imagen de perfil
        profile_picture = self.request.FILES.get('profile_picture')
        print(self.request.FILES)
        # Si se ha seleccionado una imagen de perfil, la guardamos
        if profile_picture:
            form.cleaned_data['profile_picture'] = profile_picture
        else:
            # Si no se ha seleccionado una imagen de perfil, asignamos None al campo para que no haya problemas al guardar el usuario
            #form.cleaned_data['profile_picture'] = None
            return
        
        # Guardar el usuario
        form.save()
        
        return super().form_valid(form)