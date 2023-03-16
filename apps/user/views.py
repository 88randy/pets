from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test, login_required

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from apps.user.forms import SignupForm, LoginForm

class IndexView(TemplateView):
    template_name = 'index.html'
    
    def send_mail_contact(self, name, email, message):
        subject = 'Mascota en casa: Nuevo comentario'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [settings.EMAIL_HOST_USER]
        
        # Renderizar el contenido del correo en HTML y texto plano
        html_content = render_to_string('emails/contact.html', {'name': f'{name}', 'email':email, 'message':message})
        text_content = strip_tags(html_content)

        # Crear el objeto EmailMultiAlternatives
        msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)

        # Agregar el contenido en formato HTML
        msg.attach_alternative(html_content, "text/html")

        # Enviar el correo
        msg.send()
        return
    
    def post(self, request, *args, **kwargs):
        form_data = request.POST
        try:
            self.send_mail_contact(form_data['name'], form_data['email'], form_data['message'])
            messages.success(self.request, '¡Comentarios enviados correctamente! <p><b>Gracias por tomarte el tiempo de completar el formulario, en breve nos comunicaremos contigo.</b></p>')
            return redirect(reverse('index'))
        except:
            messages.error(self.request, '¡No se pudieron enviar tus comentarios! <p><b>Ocurrió un error que no permitió enviar tus comentarios, por favor intentalo más tarde, ¡Gracias!</b></p>')
            return redirect(reverse('index'))

class SignupView(FormView):
    template_name = 'user/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('index')
    
    @method_decorator(user_passes_test(lambda user: not user.is_authenticated, login_url='index'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        # Procesa la imagen de perfil
        profile_picture = self.request.FILES.get('profile_picture')
        # Si se ha seleccionado una imagen de perfil, la guardamos
        if profile_picture:
            form.cleaned_data['profile_picture'] = profile_picture
        else:
            # Si no se ha seleccionado una imagen de perfil, asignamos None al campo para que no haya problemas al guardar el usuario
            form.cleaned_data['profile_picture'] = None
        
        # Guardar el usuario
        form.save()
        
        return super().form_valid(form)
    
class LoginView(FormView):
    template_name = 'user/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('index')
    
    @method_decorator(user_passes_test(lambda user: not user.is_authenticated, login_url='index'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        # Autenticar al usuario utilizando los datos de formulario
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Iniciar sesión para el usuario autenticado
            login(self.request, user)
            messages.success(self.request, f'Bienvenido <b>{ self.request.user }</b>, tu sesión inició exitosamente.')
            return super().form_valid(form)
        else:
            # Si las credenciales son inválidas, mostrar un mensaje de error
            form.add_error(None, 'Nombre de usuario o contraseña incorrectos')
            return self.form_invalid(form)

@method_decorator(login_required, name='dispatch')
class LogoutView(LogoutView):
    template_name = 'user/logout.html'
    success_url = reverse_lazy('login')

class InfoView(TemplateView):
    template_name = 'info.html'
    
# Custom errors

def error_404(request, exception):
    return render(request, 'errors/404.html', {})