# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0013_boton_accesibilidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boton_accesibilidad',
            name='flag',
            field=models.BooleanField(default=True),
        ),
    ]
