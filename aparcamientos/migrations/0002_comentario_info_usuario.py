# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('usuario', models.CharField(blank=True, max_length=32)),
                ('comentario', models.TextField()),
                ('hora', models.DateTimeField(default=django.utils.timezone.now)),
                ('aparcamiento', models.ForeignKey(to='aparcamientos.Aparcamiento')),
            ],
        ),
        migrations.CreateModel(
            name='Info_Usuario',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('usuario', models.CharField(blank=True, max_length=32)),
                ('hora_seleccion', models.DateTimeField(default=django.utils.timezone.now)),
                ('pagina_personal', models.CharField(blank=True, max_length=100, default='Página de usuario')),
                ('aparcamiento', models.ForeignKey(to='aparcamientos.Aparcamiento')),
            ],
        ),
    ]
