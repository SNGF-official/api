# Generated by Django 5.0.13 on 2025-04-13 12:14

import django.core.validators
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(choices=[('SEED', 'Graines'), ('PLANT', 'Plante')], max_length=10)),
                ('type', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price_per_unit', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('unit', models.CharField(blank=True, max_length=20)),
                ('quantity', models.PositiveIntegerField()),
                ('size', models.CharField(choices=[('XS', 'Très petit'), ('S', 'Petit'), ('M', 'Moyen'), ('L', 'Grand'), ('XL', 'Très grand')], max_length=5)),
                ('status', models.CharField(choices=[('ACTIVE', 'active'), ('INACTIVE', 'inactive')], max_length=10)),
                ('image_url', models.ImageField(blank=True, null=True, upload_to='plant/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])])),
            ],
        ),
        migrations.CreateModel(
            name='PlantImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='plants/gallery/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])])),
                ('alt_text', models.CharField(blank=True, max_length=255)),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='plant.plant')),
            ],
        ),
    ]
