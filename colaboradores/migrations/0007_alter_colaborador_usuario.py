# Generated by Django 5.1.7 on 2025-04-17 19:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('colaboradores', '0006_alter_colaborador_matricula'),
        ('contas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colaborador',
            name='usuario',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='colaborador', to='contas.conta'),
        ),
    ]
