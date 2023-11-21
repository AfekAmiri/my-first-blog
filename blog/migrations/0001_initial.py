# Generated by Django 2.2.28 on 2023-11-13 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lieu',
            fields=[
                ('id_lieu', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('disponibilite', models.CharField(max_length=20)),
                ('photo', models.ImageField(upload_to='ImagesLieux/')),
            ],
        ),
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('nom', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('etat', models.CharField(max_length=20)),
                ('type', models.CharField(max_length=20)),
                ('niveau', models.CharField(max_length=20)),
                ('photo', models.ImageField(upload_to='ImagesPokemons/')),
                ('lieu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Lieu')),
            ],
        ),
    ]
