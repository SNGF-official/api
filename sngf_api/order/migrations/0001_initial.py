# Generated by Django 5.0.13 on 2025-04-15 14:06

import django.db.models.deletion
import phonenumber_field.modelfields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('plant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None)),
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
