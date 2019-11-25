# Generated by Django 2.2.5 on 2019-11-25 10:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('biografia', models.TextField(help_text='biogradia')),
                ('peliculasDirigidas', models.TextField(help_text='escribir peliculas separadas por comas ')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaNacimiento', models.DateField()),
                ('categoriaPreferida', models.TextField(help_text='Categoria Pelicula')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pelicula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100, unique=True)),
                ('año', models.IntegerField()),
                ('resumen', models.TextField(help_text='Redacta un resumen sobre la pelicula')),
                ('categoria', models.TextField(help_text='Seleccione una categoria')),
                ('director', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='principal.Director')),
            ],
        ),
    ]
