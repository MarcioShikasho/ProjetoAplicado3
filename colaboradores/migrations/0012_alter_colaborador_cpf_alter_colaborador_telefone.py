# Generated by Django 5.1.7 on 2025-04-24 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('colaboradores', '0011_alter_colaborador_cpf_alter_colaborador_telefone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colaborador',
            name='cpf',
            field=models.CharField(max_length=14),
        ),
        migrations.AlterField(
            model_name='colaborador',
            name='telefone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
