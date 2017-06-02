# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0008_pagina_usuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pagina_usuario',
            name='usuario',
        ),
        migrations.RemoveField(
            model_name='info_usuario',
            name='pagina_personal',
        ),
        migrations.DeleteModel(
            name='Pagina_Usuario',
        ),
    ]
