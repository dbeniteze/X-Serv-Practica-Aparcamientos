# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0003_auto_20170522_0640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aparcamiento',
            name='identificador',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
