# Generated by Django 2.2.5 on 2020-01-07 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artista',
            fields=[
                ('idArtista', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.TextField(unique=True, verbose_name='Nombre')),
                ('url', models.URLField(verbose_name='Url del artista')),
                ('pictureUrl', models.URLField(verbose_name='Url de la imagen')),
            ],
        ),
    ]
