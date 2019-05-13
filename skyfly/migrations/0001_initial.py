# Generated by Django 2.1.7 on 2019-05-13 21:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
                ('deep_link', models.URLField()),
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
                ('request_hash', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='kiwiresponse',
            name='skyfly_request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='skyfly.SkyflyRequest'),
        ),
    ]
