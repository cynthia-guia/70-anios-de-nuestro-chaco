# Generated by Django 3.2.6 on 2021-08-29 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0011_auto_20210829_0343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preguntasrespondidas',
            name='respuesta',
        ),
        migrations.AddField(
            model_name='preguntasrespondidas',
            name='respuesta',
            field=models.ManyToManyField(null=True, to='Quiz.Respuesta'),
        ),
        migrations.DeleteModel(
            name='RespuestasList',
        ),
    ]
