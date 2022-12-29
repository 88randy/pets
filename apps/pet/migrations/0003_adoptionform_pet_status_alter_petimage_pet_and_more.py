# Generated by Django 4.1.4 on 2022-12-29 01:31

import apps.pet.validations
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pet', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdoptionForm',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('second_last_name', models.CharField(max_length=100, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=12, validators=[apps.pet.validations.validate_phone])),
                ('country', models.CharField(default='México', max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('town', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=5)),
                ('address', models.CharField(max_length=250)),
                ('message', models.TextField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='pet',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='petimage',
            name='pet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pet_images', to='pet.pet'),
        ),
        migrations.CreateModel(
            name='AdoptionRequest',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('S', 'Sent'), ('A', 'Approved'), ('R', 'Rejected')], max_length=1)),
                ('adoption_form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='form_adoption_requests', to='pet.adoptionform')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pet_adoption_requests', to='pet.pet')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
