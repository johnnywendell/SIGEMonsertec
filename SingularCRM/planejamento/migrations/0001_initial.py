# Generated by Django 5.0.4 on 2024-05-15 18:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cadastro', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='AS',
            fields=[
                ('timestampedmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cadastro.timestampedmodel')),
                ('data', models.DateField(verbose_name='Período')),
                ('escopo', models.CharField(max_length=120, verbose_name='Escopo do serviço')),
                ('local', models.CharField(max_length=80, verbose_name='Local do serviço')),
                ('tipo', models.CharField(choices=[('PARADA', 'PARADA'), ('PACOTE', 'PACOTE'), ('ROTINA', 'ROTINA'), ('PROJETO', 'PROJETO')], max_length=20, verbose_name='Tipo Serviço')),
                ('doc', models.FileField(blank=True, null=True, upload_to='planejamento/', verbose_name='documento')),
                ('slug', models.SlugField(default='')),
                ('disciplina', models.CharField(choices=[('ANDAIME', 'ANDAIME'), ('PINTURA', 'PINTURA'), ('ISOLAMENTO', 'ISOLAMENTO'), ('GERAL', 'GERAL')], max_length=20)),
                ('obs', models.TextField(blank=True, null=True, verbose_name='Obs')),
                ('aprovado', models.BooleanField(default=False)),
                ('contrato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastro.contrato')),
                ('solicitante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cadastro.solicitante')),
                ('unidade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cadastro.area')),
            ],
            options={
                'ordering': ('-pk',),
            },
            bases=('cadastro.timestampedmodel',),
        ),
        migrations.CreateModel(
            name='ProjetoCodigo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projeto_nome', models.CharField(max_length=30, unique=True)),
                ('contrato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastro.contrato')),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='RDO',
            fields=[
                ('timestampedmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cadastro.timestampedmodel')),
                ('data', models.DateField(verbose_name='Período')),
                ('escopo', models.CharField(max_length=120, verbose_name='Escopo do serviço')),
                ('local', models.CharField(max_length=80, verbose_name='Local do serviço')),
                ('tipo', models.CharField(choices=[('PARADA', 'PARADA'), ('PACOTE', 'PACOTE'), ('ROTINA', 'ROTINA'), ('PROJETO', 'PROJETO')], max_length=20, verbose_name='Tipo Serviço')),
                ('doc', models.FileField(blank=True, null=True, upload_to='planejamento/', verbose_name='documento')),
                ('slug', models.SlugField(default='')),
                ('disciplina', models.CharField(choices=[('ANDAIME', 'ANDAIME'), ('PINTURA', 'PINTURA'), ('ISOLAMENTO', 'ISOLAMENTO'), ('GERAL', 'GERAL')], max_length=20)),
                ('obs', models.TextField(blank=True, null=True, verbose_name='Obs')),
                ('aprovado', models.BooleanField(default=False)),
                ('encarregado', models.CharField(max_length=40, verbose_name='Encarregado')),
                ('clima', models.CharField(choices=[('BOM', 'BOM'), ('NUBLADO', 'NUBLADO'), ('CHUVOSO', 'CHUVOSO')], max_length=20, verbose_name='Clima')),
                ('inicio', models.TimeField(blank=True, null=True, verbose_name='Inicio')),
                ('termino', models.TimeField(blank=True, null=True, verbose_name='Fim')),
                ('inicio_pt', models.TimeField(blank=True, null=True, verbose_name='Inicio PT')),
                ('termino_pt', models.TimeField(blank=True, null=True, verbose_name='Término PT')),
                ('AS', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ass', to='planejamento.as', verbose_name='AS')),
                ('contrato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastro.contrato')),
                ('projeto_cod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='planejamento.projetocodigo', verbose_name='Cód. Projetos')),
                ('solicitante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cadastro.solicitante')),
                ('unidade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cadastro.area')),
            ],
            options={
                'ordering': ('-pk',),
            },
            bases=('cadastro.timestampedmodel',),
        ),
        migrations.CreateModel(
            name='ItemMedicao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qtd', models.DecimalField(decimal_places=3, max_digits=12, verbose_name='qtd')),
                ('total', models.DecimalField(decimal_places=3, max_digits=12, verbose_name='total')),
                ('efetivo', models.DecimalField(blank=True, decimal_places=3, max_digits=12, null=True, verbose_name='Efetivo')),
                ('qtd_t', models.DecimalField(blank=True, decimal_places=3, max_digits=12, null=True, verbose_name='Tubo')),
                ('qtd_e', models.DecimalField(blank=True, decimal_places=3, max_digits=12, null=True, verbose_name='Encaixe')),
                ('qtd_pranchao', models.DecimalField(blank=True, decimal_places=3, max_digits=12, null=True, verbose_name='Pranchão')),
                ('qtd_piso', models.DecimalField(blank=True, decimal_places=3, max_digits=12, null=True, verbose_name='Piso')),
                ('montagem', models.CharField(blank=True, choices=[('MONTAGEM', 'MONTAGEM'), ('DESMONTAGEM', 'DESMONTAGEM')], max_length=20, null=True, verbose_name='Tipo')),
                ('placa', models.CharField(blank=True, max_length=30, null=True, verbose_name='Placa')),
                ('item_contrato', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cadastro.itembm')),
                ('doc_origem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rdos', to='planejamento.rdo')),
            ],
        ),
    ]
