# Generated by Django 3.2.3 on 2021-05-28 02:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='technician',
            old_name='technicial_name',
            new_name='technician_name',
        ),
    ]
