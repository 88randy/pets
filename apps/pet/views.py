from django.urls import reverse
from django.conf import settings
from django.db import transaction
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.db.models import OuterRef, Subquery, Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, ListView

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from apps.pet.forms import PetForm, ImageForm, AdoptionFormF
from apps.pet.models import Pet, PetImage, AdoptionRequest, AdoptionForm
from apps.pet.filters import PetFilter

from api.cp import PostalCodeAPI

# Create your views here.

@method_decorator(login_required, name='dispatch')
class PetCreateView(CreateView):
    template_name = 'pet/create_pet.html'
    form_class = PetForm
    success_url = '/mascota/crear/correcto'
    
    def user_is_adopter(self):
        user = self.request.user
        # Verificar si el tipo de usuario es 'A'
        has_type_A = user.type_user == 'A'
        return has_type_A
        
    def dispatch(self, request, *args, **kwargs):
        if self.user_is_adopter():
            messages.error(self.request, '¡Tu nivel de usuario no te permite subir información de mascotas! <p>Si deseas dar en adopción una mascota contactanos para asistire.</p><p><b>randy88allan@gmail.com</b></p><p><h3>¡Gracias!</h3></p>')
            return redirect(reverse('index'))
        
        if request.method.lower() in self.http_method_names:
            handler = getattr(
                self, request.method.lower(), self.http_method_not_allowed
            )
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)
    
    @transaction.atomic
    def form_valid(self, form):
        self.object = form.save()
        user = self.request.user
        image_list = self.request.FILES.getlist('images')
        for image in image_list:
            pet_image = PetImage(
                    created_by = user,
                    modified_by = user,
                    pet = self.object, 
                    image = image
                )
            pet_image.save()
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        if "form" not in kwargs:
            kwargs["form"] = self.get_form()
        kwargs["images_form"] = ImageForm
        return super().get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    """ def get_success_url(self):
        return reverse('pet_created', args=(self.object.pk,)) """

class PetDetailView(DetailView):
    model = Pet
    template_name='pet/pet_detail.html'
    
    def adoption_form_exists(self):
        pet_id = self.object.pk
        user_id = self.request.user.pk

        adoption_form = AdoptionForm.objects.filter(
            Q(form_adoption_requests__pet_id = pet_id) & Q(created_by = user_id)
        ).first()
        return adoption_form
    
    def get_pictures_pet(self):
        return self.object.pet_images.all()
    
    def get_context_data(self, **kwargs):
        context = {}
        if self.object:
            context["object"] = self.object
            context['object_pictures'] = self.get_pictures_pet()
            context['adoption_form_exists'] = self.adoption_form_exists()
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
        context.update(kwargs)
        return super().get_context_data(**context)

@method_decorator(login_required, name='dispatch')
class MyPetListView(ListView):
    model = Pet
    template_name = 'pet/pet_list.html'
    
    def get_queryset(self):
        # Subconsulta para obtener la primera imagen de cada mascota
        subquery = PetImage.objects.filter(pet=OuterRef('pk')).order_by('pk').values('image')[:1]
        
        # Anotar la subconsulta al queryset original
        queryset = self.model.objects.filter(created_by=self.request.user).annotate(first_image=Subquery(subquery))
        
        return queryset

class ListOfPetsForAdoptionView(ListView):
    model = Pet
    filterset_class = PetFilter
    paginate_by = 6
    template_name = 'pet/list_of_pets_for_adoption.html'
    
    def get_queryset(self):
        subquery = PetImage.objects.filter(pet=OuterRef('pk')).order_by('pk').values('image')[:1]
        queryset = self.model.objects.filter(status=True).annotate(first_image=Subquery(subquery))
        
        # Filter queryset based on request GET parameters
        pet_filter = PetFilter(self.request.GET, queryset=queryset)
        return pet_filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PetFilter(self.request.GET, queryset=self.get_queryset())

        queryset = self.get_queryset()
        paginator = Paginator(queryset, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        
        return context

@method_decorator(login_required, name='dispatch')
class AdoptionFormView(CreateView):
    template_name = 'pet/adoption_form.html'
    form_class = AdoptionFormF
    
    def adoption_form_exists(self):
        pet_id = self.get_pet().pk
        user_id = self.request.user.pk

        adoption_form = AdoptionForm.objects.filter(
            Q(form_adoption_requests__pet_id = pet_id) & Q(created_by = user_id)
        ).first()
        return adoption_form
    
    def dispatch(self, request, *args, **kwargs):
        if self.adoption_form_exists():
            messages.warning(self.request, '¡Ya haz enviado una solicitud de adopción para esta mascota! <p>Si luego de 48 horas de enviada tu solicitud aún no te ha contactado un miembro de nuestro equipo te pedimos por favor nos envíes un correo electróncio para asistire.</p><p><b>randy88allan@gmail.com</b></p><p><h3>¡Gracias!</h3></p>')
            return redirect(reverse('list_of_pets_for_adoption'))
        
        if request.method.lower() in self.http_method_names:
            handler = getattr(
                self, request.method.lower(), self.http_method_not_allowed
            )
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)
    
    def get_pet(self):
        pet = Pet.objects.filter(pk = self.kwargs['pk']).first()
        return pet
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_pet(self):
        pet_uuid = self.kwargs['pk']
        subquery = PetImage.objects.filter(pet=OuterRef('pk')).order_by('pk').values('image')[:1]
        pet = Pet.objects.filter(pk = pet_uuid).annotate(first_image = Subquery(subquery)).first()
        return pet
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pet'] = self.get_pet()
        return context
    
    def send_mail_adoption(self, to_email, name):
        subject = 'Mascota en casa: Solicitud de adopción enviada'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [to_email]
        bcc_list = [settings.EMAIL_HOST_USER]#settings.BCC_LIST
        
        # Renderizar el contenido del correo en HTML y texto plano
        html_content = render_to_string('emails/adoption.html', {'name': f'{name}', 'pet':self.get_pet().name})
        text_content = strip_tags(html_content)

        # Crear el objeto EmailMultiAlternatives
        msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list, bcc = bcc_list)

        # Agregar el contenido en formato HTML
        msg.attach_alternative(html_content, "text/html")

        # Enviar el correo
        msg.send()
        return
    
    def send_data_mail_adoption(self, form, pet, user, request_form):
        subject = f'Mascota en casa: Solicitud de adopción {request_form.pk}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [settings.EMAIL_HOST_USER]
        
        # Renderizar el contenido del correo en HTML y texto plano
        html_content = render_to_string('emails/adoption_data.html', {
                            'form': form,
                            'pet': pet,
                            'user': user,
                            'request_form': request_form
                            }
                        )
        text_content = strip_tags(html_content)

        # Crear el objeto EmailMultiAlternatives
        msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)

        # Agregar el contenido en formato HTML
        msg.attach_alternative(html_content, "text/html")

        # Enviar el correo
        msg.send()
        return
    
    @transaction.atomic
    def form_valid(self, form):
        # Guardar los datos del modelo en la base de datos
        self.object = form.save()
        user = self.request.user
        email = self.object.email
        name = self.object.name
        adoption_request = AdoptionRequest(
            created_by = user,
            modified_by = user,
            pet = self.get_pet(),
            adoption_form = self.object,
            status = 'S'
        )
        adoption_request.save()
        self.send_mail_adoption(email, name)
        self.send_data_mail_adoption(self.object, self.get_pet(), user, adoption_request)
        # Mostrar mensaje de éxito
        messages.success(self.request, '¡Solicitud de adopción enviada correctamente! <p>Por favor verifica tu bandeja de entrada del correo electrónico donde encontrarás más información.</p> \n <p><b>Gracias por tomarte el tiempo de completar el formulario, en breve nos comunicaremos contigo.</b></p>')
        
        # Redirigir al usuario al index
        return redirect(reverse('index'))

# Other views
@login_required
def get_postal_details(request, postal_code):
    if len(postal_code) != 5 or not postal_code.isdigit():
        return JsonResponse({'mensaje': 'El codigo postal debe constar de 5 números.'}, status=404)
    
    fetcher = PostalCodeAPI()
    postal_code_info = fetcher.get_postal_code(postal_code)
    if postal_code_info:
        # devuelve la información en un JSON para que pueda ser manejado en el frontend
        return JsonResponse(postal_code_info, status=200)
    else:
        return JsonResponse({'mensaje': 'No se encontró la información del código postal.'}, status=404)
    
# Success forms
@login_required
def success_create_pet(request):
    return render(request, 'pet/success_create_pet.html')