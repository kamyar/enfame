# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meddit', '0002_urlentry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='urlentry',
            name='id',
        ),
        migrations.AlterField(
            model_name='urlentry',
            name='extension',
            field=models.CharField(max_length=100, serialize=False, primary_key=True),
            preserve_default=True,
        ),
    ]
