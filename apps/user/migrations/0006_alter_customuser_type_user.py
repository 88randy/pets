# Generated by Django 4.1.4 on 2023-03-09 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_customuser_type_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='type_user',
            field=models.CharField(choices=[('A', 'Quiero Adoptar'), ('Q', 'Quiero dar en Adopción'), ('O', 'Somos una Organización')], max_length=1),
        ),
    ]