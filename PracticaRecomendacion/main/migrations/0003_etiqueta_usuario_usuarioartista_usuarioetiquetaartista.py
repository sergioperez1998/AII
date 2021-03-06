# Generated by Django 2.2.5 on 2020-01-07 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20200107_2119'),
    ]

    operations = [
        migrations.CreateModel(
            name='Etiqueta',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('tagValue', models.TextField(unique=True, verbose_name='Valor de la tag')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('idUsuario', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='UsuarioEtiquetaArtista',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('idArtista', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Artista')),
                ('idTag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Etiqueta')),
                ('idUsuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Usuario')),
            ],
        ),
        migrations.CreateModel(
            name='UsuarioArtista',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tiempoEscucha', models.IntegerField()),
                ('idArtista', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Artista')),
                ('idUsuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Usuario')),
            ],
        ),
    ]
