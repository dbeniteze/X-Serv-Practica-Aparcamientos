# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0015_delete_boton_accesibilidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='aparcamiento',
            name='puntuacion',
            field=models.IntegerField(default=0),
        ),
    ]
