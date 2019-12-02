# Generated by Django 2.1.2 on 2019-11-28 09:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='puntuacion',
            options={'ordering': ('idPelicula', 'idUsuario')},
        ),
        migrations.AlterField(
            model_name='puntuacion',
            name='puntuacion',
            field=models.IntegerField(choices=[(1, 'Muy mala'), (2, 'Mala'), (3, 'Regular'), (4, 'Buena'), (5, 'Muy Buena')], validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], verbose_name='Puntuación'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='edad',
            field=models.IntegerField(help_text='Debe introducir una edad', verbose_name='Edad'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='ocupacion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Ocupacion'),
        ),
    ]
