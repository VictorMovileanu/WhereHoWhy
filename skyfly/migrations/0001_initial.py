# Generated by Django 2.1.7 on 2019-06-08 10:54

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KiwiException',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('exception_message', models.TextField()),
                ('data', models.TextField()),
                ('traceback', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='KiwiResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('departure', models.DateTimeField(null=True)),
                ('arrival', models.DateTimeField(null=True)),
                ('city', models.CharField(max_length=100)),
                ('price', models.PositiveIntegerField()),
                ('trip_duration', models.PositiveIntegerField(verbose_name='Trip duration in seconds')),
                ('deep_link', models.URLField(max_length=2083)),
                ('color', models.CharField(max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SkyflyRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('unique_id', models.UUIDField(default=uuid.uuid1, editable=False, unique=True)),
                ('start', models.CharField(default='MUC', max_length=3)),
                ('left_combinations', models.PositiveIntegerField(verbose_name='Number of different date-destination combinations left to query')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='kiwiresponse',
            name='skyfly_request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flights', to='skyfly.SkyflyRequest'),
        ),
        migrations.AddField(
            model_name='kiwiexception',
            name='skyfly_request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exceptions', to='skyfly.SkyflyRequest'),
        ),
    ]
