# Generated by Django 2.2.5 on 2020-01-13 17:39

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Libro',
            fields=[
                ('bookId', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.TextField(unique=True, verbose_name='Titulo')),
                ('autor', models.TextField(verbose_name='Autor')),
                ('genero', models.TextField(verbose_name='Genero')),
                ('idioma', models.TextField(verbose_name='Idioma')),
                ('puntuaciones', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('idUsuario', models.TextField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Puntuacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntuacion', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('IdUsuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Usuario')),
                ('bookId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Libro')),
            ],
        ),
    ]
