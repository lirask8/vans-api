# Generated by Django 3.0.5 on 2020-12-18 07:30

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_auto_20201218_0730'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.CharField(editable=False, max_length=22, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=10, unique=True, verbose_name='Code')),
                ('name', models.CharField(max_length=50, verbose_name='Status name')),
            ],
            options={
                'verbose_name': 'Status',
                'verbose_name_plural': 'Status',
                'db_table': 'status',
            },
        ),
        migrations.CreateModel(
            name='Van',
            fields=[
                ('id', models.CharField(editable=False, max_length=22, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('plates', models.CharField(max_length=7, unique=True, verbose_name='Plates')),
                ('economic_number', models.CharField(max_length=7, verbose_name='Economic Number')),
                ('seats', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Seats')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='vans.Status', verbose_name='Status')),
            ],
            options={
                'verbose_name': 'Van',
                'verbose_name_plural': 'Vans',
                'db_table': 'van',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.CharField(editable=False, max_length=22, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('final_status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='final', to='vans.Status', verbose_name='Final Status')),
                ('initial_status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='initial', to='vans.Status', verbose_name='Initial Status')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.User', verbose_name='User')),
                ('van', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vans.Van', verbose_name='Van')),
            ],
            options={
                'verbose_name': 'Log',
                'verbose_name_plural': 'Logs',
                'db_table': 'log',
            },
        ),
    ]
