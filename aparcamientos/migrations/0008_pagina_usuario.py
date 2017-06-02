# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0007_auto_20170524_0121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pagina_Usuario',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('pagina_personal', models.CharField(default='Página de ', max_length=100, blank=True)),
                ('usuario', models.ForeignKey(to='aparcamientos.Info_Usuario')),
            ],
        ),
    ]
