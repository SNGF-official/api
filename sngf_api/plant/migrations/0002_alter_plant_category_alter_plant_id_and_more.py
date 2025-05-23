# Generated by Django 5.0.13 on 2025-04-16 13:17

import uuid

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('plant', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='category',
            field=models.CharField(blank=True, choices=[('AGROFORESTIERES', 'Agroforestières'),
                                                        ('ENDEMIQUES_AUTOCHTONES', 'Endémiques autochtones'),
                                                        ('EXOTIQUES_REBOISEMENT', 'Exotiques de reboisement'),
                                                        ('ORNEMENTALES', 'Ornementales'),
                                                        ('EMBROUSSAILLEMENTS', 'Embrousseillements')],
                                   help_text='La catégorie du produit.Vous pouvez choisir parmi les options proposées.',
                                   max_length=30),
        ),
        migrations.AlterField(
            model_name='plant',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False,
                                   help_text='Identifiant unique du produit de base.Il est généré automatiquement et ne peut pas être modifié.',
                                   primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='plantimage',
            name='alt_text',
            field=models.CharField(blank=True,
                                   help_text="Texte alternatif pour l'image,important pour l'accessibilité et le SEO.",
                                   max_length=255),
        ),
        migrations.AlterField(
            model_name='plantimage',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False,
                                   help_text="Identifiant unique de l'image de la plante.Il est généré automatiquement et ne peut pas être modifié.",
                                   primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='plantimage',
            name='image',
            field=models.ImageField(
                help_text='Le fichier image de la plante.Les formats supportés sont JPG, JPEG, PNG et WEBP.',
                upload_to='plants/gallery/',
                validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])]),
        ),
        migrations.CreateModel(
            name='SeedImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False,
                                        help_text="Identifiant unique de l'image de la graine.Il est généré automatiquement et ne peut pas être modifié.",
                                        primary_key=True, serialize=False)),
                ('image', models.ImageField(
                    help_text='Le fichier image de la plante.Les formats supportés sont JPG, JPEG, PNG et WEBP.',
                    upload_to='seeds/gallery/',
                    validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])])),
                ('alt_text', models.CharField(blank=True,
                                              help_text="Texte alternatif pour l'image,important pour l'accessibilité et le SEO.",
                                              max_length=255)),
                ('seed', models.ForeignKey(help_text='La graîne à laquelle cette image est associée.',
                                           on_delete=django.db.models.deletion.CASCADE, related_name='images',
                                           to='plant.seed')),
            ],
        ),
    ]
