# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0006_auto_20170523_0801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info_usuario',
            name='pagina_personal',
            field=models.CharField(default='Página de ', blank=True, max_length=100),
        ),
    ]
