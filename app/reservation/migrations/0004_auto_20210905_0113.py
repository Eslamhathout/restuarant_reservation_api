# Generated by Django 2.1.15 on 2021-09-05 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0003_auto_20210903_2226'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='end_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='start_time',
            field=models.TimeField(),
        ),
    ]
