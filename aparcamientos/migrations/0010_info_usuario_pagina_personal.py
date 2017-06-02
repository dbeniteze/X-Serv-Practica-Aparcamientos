# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0009_auto_20170524_0806'),
    ]

    operations = [
        migrations.AddField(
            model_name='info_usuario',
            name='pagina_personal',
            field=models.CharField(default='PAGINA DE ', blank=True, max_length=200),
        ),
    ]
