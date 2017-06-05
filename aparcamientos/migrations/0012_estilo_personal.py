# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0011_remove_info_usuario_pagina_personal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estilo_Personal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('usuario', models.CharField(blank=True, max_length=32)),
                ('nombre_pagina', models.CharField(blank=True, max_length=200)),
                ('tamaño_letra', models.IntegerField(default='140')),
                ('color', models.CharField(default='#FFFFFF', max_length=20)),
            ],
        ),
    ]
