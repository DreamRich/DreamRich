# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-10 04:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegularCosts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home', models.DecimalField(decimal_places=2, max_digits=8)),
                ('electricity_bill', models.DecimalField(decimal_places=2, max_digits=8)),
                ('gym', models.DecimalField(decimal_places=2, max_digits=8)),
                ('taxes', models.DecimalField(decimal_places=2, max_digits=8)),
                ('car_gas', models.DecimalField(decimal_places=2, max_digits=8)),
                ('insurance', models.DecimalField(decimal_places=2, max_digits=8)),
                ('cellphone', models.DecimalField(decimal_places=2, max_digits=8)),
                ('health_insurance', models.DecimalField(decimal_places=2, max_digits=8)),
                ('supermarket', models.DecimalField(decimal_places=2, max_digits=8)),
                ('housekeeper', models.DecimalField(decimal_places=2, max_digits=8)),
                ('beauty', models.DecimalField(decimal_places=2, max_digits=8)),
                ('internet', models.DecimalField(decimal_places=2, max_digits=8)),
                ('netflix', models.DecimalField(decimal_places=2, max_digits=8)),
                ('recreation', models.DecimalField(decimal_places=2, max_digits=8)),
                ('meals', models.DecimalField(decimal_places=2, max_digits=8)),
                ('appointments', models.DecimalField(decimal_places=2, max_digits=8)),
                ('drugstore', models.DecimalField(decimal_places=2, max_digits=8)),
                ('extras', models.DecimalField(decimal_places=2, max_digits=8)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.Client')),
            ],
        ),
    ]
