# Generated by Django 4.2.2 on 2023-06-22 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_usac', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pelicula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('categoria', models.CharField(max_length=50)),
                ('imagen', models.ImageField(upload_to='peliculas/')),
            ],
        ),
    ]
