# Generated by Django 2.2.28 on 2022-08-24 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inmessages',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
        migrations.AlterField(
            model_name='messages',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]