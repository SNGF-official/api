# Generated by Django 5.0.13 on 2025-05-11 07:00

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_alter_orderitem_product_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='product_id',
            field=models.UUIDField(default=uuid.UUID('f85c1bff-7e26-40e4-91fc-3aac140a8e50')),
        ),
    ]
