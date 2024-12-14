# Generated by Django 5.1.4 on 2024-12-14 04:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_carrera', models.CharField(max_length=10, unique=True)),
                ('nombre_carrera', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_curso', models.CharField(max_length=10, unique=True)),
                ('nombre_curso', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dni', models.CharField(max_length=8, unique=True)),
                ('correo_electronico', models.CharField(default='no especificado', max_length=200)),
                ('nombre_completo', models.CharField(default='no especificado', max_length=200)),
                ('nombre_carrera', models.CharField(blank=True, max_length=255, null=True)),
                ('nombres', models.CharField(default='no especificado', max_length=200)),
                ('apellido_paterno', models.CharField(default='no especificado', max_length=200)),
                ('apellido_materno', models.CharField(default='no especificado', max_length=200)),
                ('numero_telefono', models.CharField(blank=True, max_length=15, null=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('codigo_carrera', models.CharField(blank=True, max_length=10, null=True)),
                ('tipo_usuario', models.CharField(default='no especificado', max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil_alumno', to=settings.AUTH_USER_MODEL)),
                ('carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autenticacion.carrera')),
            ],
        ),
        migrations.CreateModel(
            name='MiPerfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dni', models.CharField(max_length=8, unique=True)),
                ('tipo_usuario', models.CharField(default='no especificado', max_length=50)),
                ('nombre_usuario', models.CharField(default='no especificado', max_length=200)),
                ('correo_electronico', models.CharField(default='no especificado', max_length=200)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('numero_telefono', models.CharField(blank=True, max_length=15, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil_mi', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dni', models.CharField(max_length=8, unique=True)),
                ('correo_electronico', models.CharField(default='no especificado', max_length=200)),
                ('nombre_completo', models.CharField(default='no especificado', max_length=200)),
                ('nombres', models.CharField(default='no especificado', max_length=200)),
                ('apellido_paterno', models.CharField(default='no especificado', max_length=200)),
                ('apellido_materno', models.CharField(default='no especificado', max_length=200)),
                ('numero_telefono', models.CharField(blank=True, max_length=9, null=True)),
                ('capacitaciones', models.TextField(blank=True, default='No hay capacitaciones', null=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('retroalimentacion', models.TextField(blank=True, default='Agregar retroalimentación', null=True)),
                ('tipo_usuario', models.CharField(default='profesor(a)', max_length=50)),
                ('pdf_reporte', models.FileField(blank=True, null=True, upload_to='pdf_reports/')),
                ('cursos', models.ManyToManyField(related_name='profesores', to='autenticacion.curso')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil_profesor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Supervisor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dni', models.CharField(max_length=8, unique=True)),
                ('correo_electronico', models.CharField(default='no especificado', max_length=200)),
                ('nombre_completo', models.CharField(default='no especificado', max_length=200)),
                ('nombres', models.CharField(default='no especificado', max_length=200)),
                ('apellido_paterno', models.CharField(default='no especificado', max_length=200)),
                ('apellido_materno', models.CharField(default='no especificado', max_length=200)),
                ('numero_telefono', models.CharField(blank=True, max_length=9, null=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('tipo_usuario', models.CharField(default='supervisor(a)', max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil_supervisor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]