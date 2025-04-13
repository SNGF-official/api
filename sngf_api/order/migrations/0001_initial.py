# Generated by Django 5.0.13 on 2025-04-13 13:04

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('plant', '0002_remove_plant_image_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('customer_email', models.EmailField(blank=True, max_length=254)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('PENDING', 'En attente'), ('CONFIRMED', 'Confirmée'), ('CANCELLED', 'Annulée')], default='PENDING', max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='order.order')),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plant.plant')),
            ],
            options={
                'unique_together': {('order', 'plant')},
            },
        ),
    ]
