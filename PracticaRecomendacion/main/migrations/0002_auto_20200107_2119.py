# Generated by Django 2.2.5 on 2020-01-07 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artista',
            name='idArtista',
            field=models.TextField(primary_key=True, serialize=False),
        ),
    ]