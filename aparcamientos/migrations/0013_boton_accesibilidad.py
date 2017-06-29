# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0012_estilo_personal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boton_Accesibilidad',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('estado', models.CharField(max_length=32, default='estado')),
                ('flag', models.BooleanField(default=False)),
            ],
        ),
    ]
