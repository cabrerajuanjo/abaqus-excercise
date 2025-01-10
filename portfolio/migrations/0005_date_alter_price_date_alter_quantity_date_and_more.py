# Generated by Django 5.1.4 on 2025-01-09 16:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0004_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
        ),
        migrations.AlterField(
            model_name='price',
            name='date',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='portfolio.date'),
        ),
        migrations.AlterField(
            model_name='quantity',
            name='date',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='portfolio.date'),
        ),
        migrations.AlterField(
            model_name='weight',
            name='date',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='portfolio.date'),
        ),
    ]
