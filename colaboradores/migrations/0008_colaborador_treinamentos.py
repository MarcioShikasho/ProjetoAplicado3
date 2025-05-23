# Generated by Django 5.1.7 on 2025-04-22 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('colaboradores', '0007_alter_colaborador_usuario'),
        ('treinamentos', '0004_remove_treinamento_colaborador_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='colaborador',
            name='treinamentos',
            field=models.ManyToManyField(blank=True, related_name='colaboradores', through='colaboradores.TreinamentoColaborador', to='treinamentos.treinamento'),
        ),
    ]
