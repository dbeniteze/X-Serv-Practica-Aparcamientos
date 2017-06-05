# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0010_info_usuario_pagina_personal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='info_usuario',
            name='pagina_personal',
        ),
    ]
