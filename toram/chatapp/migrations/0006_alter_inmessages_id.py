# Generated by Django 4.0.5 on 2022-08-08 08:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0005_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inmessages',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]
