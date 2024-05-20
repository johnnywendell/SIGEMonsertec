from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from core.custom_views import CustomCreateView, CustomUpdateView, CustomTemplateView, CustomListView, CustomView
from django.http import JsonResponse
from .models import PlanoContasGrupo, PlanoContasSubgrupo, Lancamento, Saida, Entrada, MovimentoCaixa
from .forms import PlanoContasGrupoForm, PlanoContasSubgrupoFormSet, ContaPagarForm, ContaReceberForm, SaidaForm, EntradaForm
from itertools import chain
from datetime import datetime, date
import calendar


#######################################################################
############## PLANOS DE CONTAS #######################################
#######################################################################

class PlanoContasView(CustomTemplateView):
    template_name = "plano.html"
    success_url = reverse_lazy('financeiro:planocontasview')
    permission_codename = 'view_planocontasgrupo'

    def get_context_data(self, **kwargs):
        context = super(PlanoContasView, self).get_context_data(**kwargs)
        grupo_entrada = []
        grupo_saida = []

        for grupo in PlanoContasGrupo.objects.all():
            if grupo.tipo_grupo == '0' and '.' not in grupo.codigo:
                grupo_entrada.append(grupo)
            elif grupo.tipo_grupo == '1' and '.' not in grupo.codigo:
                grupo_saida.append(grupo)

        context['all_grupos_entrada'] = grupo_entrada
        context['all_grupos_saida'] = grupo_saida
        return context

    # Remover items selecionados da database
    def post(self, request, *args, **kwargs):
        if self.check_user_delete_permission(request, PlanoContasGrupo):
            for key, value in request.POST.items():
                if value == 'on':
                    grupo = None
                    subgrupo = False
                    tipo = None
                    try:
                        instance = PlanoContasSubgrupo.objects.get(id=key)
                        grupo = instance.grupo
                        subgrupo = True
                    except PlanoContasGrupo.DoesNotExist:
                        instance = PlanoContasGrupo.objects.get(id=key)
                        grupo = instance

                    tipo = instance.tipo_grupo
                    instance.delete()

                    # Reordenar codigos dos subgrupos
                    if grupo and subgrupo:
                        for i, obj in enumerate(PlanoContasSubgrupo.objects.filter(grupo=grupo), start=1):
                            obj.codigo = str(grupo.codigo) + '.' + str(i)
                            obj.save()
                    # Reordenar codigos dos grupos e subgrupos
                    else:
                        id_list = []
                        for g in PlanoContasGrupo.objects.filter(tipo_grupo=tipo):
                            if not PlanoContasSubgrupo.objects.filter(id=g.id).count():
                                id_list.append(g.id)

                        for i, obj in enumerate(PlanoContasGrupo.objects.filter(pk__in=id_list), start=1):
                            obj.codigo = str(i)
                            obj.save()
                            for j, subobj in enumerate(PlanoContasSubgrupo.objects.filter(grupo=obj), start=1):
                                subobj.codigo = str(obj.codigo) + '.' + str(j)
                                subobj.save()
        return redirect(self.success_url)
    
class AdicionarGrupoPlanoContasView(CustomCreateView):
    form_class = PlanoContasGrupoForm
    template_name = "grupo_add.html"
    success_url = reverse_lazy('financeiro:planocontasview')
    success_message = "Grupo <b>%(descricao)s </b>adicionado com sucesso."
    permission_codename = 'add_planocontasgrupo'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, descricao=self.object.descricao)

    def get(self, request, *args, **kwargs):
        self.object = None
        form = PlanoContasGrupoForm(prefix='grupo_form')

        subgrupo_form = PlanoContasSubgrupoFormSet(prefix='subgrupo_form')
        subgrupo_form.can_delete = False

        return self.render_to_response(self.get_context_data(form=form, formset=subgrupo_form))

    def post(self, request, *args, **kwargs):
        self.object = None
        form = PlanoContasGrupoForm(request.POST, prefix='grupo_form')

        subgrupo_form = PlanoContasSubgrupoFormSet(
            request.POST, prefix='subgrupo_form')

        if (form.is_valid() and subgrupo_form.is_valid()):
            self.object = form.save(commit=False)
            n_subgrupos = PlanoContasSubgrupo.objects.filter(
                tipo_grupo=self.object.tipo_grupo).count()
            n_grupos = PlanoContasGrupo.objects.filter(
                tipo_grupo=self.object.tipo_grupo).count()

            self.object.codigo = n_grupos - n_subgrupos + 1
            self.object.save()

            subgrupo_form.instance = self.object
            objs = subgrupo_form.save()

            for i, obj in enumerate(objs, start=1):
                obj.codigo = str(self.object.codigo) + '.' + str(i)
                obj.tipo_grupo = self.object.tipo_grupo
                obj.save()

            return self.form_valid(form)

        return self.form_invalid(form=form, subgrupo_form=subgrupo_form)


class EditarGrupoPlanoContasView(CustomUpdateView):
    form_class = PlanoContasGrupoForm
    model = PlanoContasGrupo
    template_name = "grupo_edit.html"
    success_url = reverse_lazy('financeiro:planocontasview')
    success_message = "Grupo <b>%(descricao)s </b>editado com sucesso."
    permission_codename = 'change_planocontasgrupo'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, descricao=self.object.descricao)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        subgrupo_form = PlanoContasSubgrupoFormSet(
            instance=self.object, prefix='subgrupo_form')
        subgrupos = PlanoContasSubgrupo.objects.filter(grupo=self.object)

        if len(subgrupos):
            subgrupo_form.extra = 0

        return self.render_to_response(self.get_context_data(form=form, formset=subgrupo_form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        subgrupo_form = PlanoContasSubgrupoFormSet(
            request.POST, prefix='subgrupo_form', instance=self.object)

        if (form.is_valid() and subgrupo_form.is_valid()):
            self.object = form.save(commit=False)
            self.object.save()

            subgrupo_form.instance = self.object
            subgrupo_form.save()

            for i, obj in enumerate(PlanoContasSubgrupo.objects.filter(grupo=self.object), start=1):
                obj.codigo = str(self.object.codigo) + '.' + str(i)
                obj.tipo_grupo = self.object.tipo_grupo
                obj.save()

            return self.form_valid(form)

        return self.form_invalid(form=form, subgrupo_form=subgrupo_form)
    
#######################################################################
############## MOVIMENTAÇÕES ##########################################
#######################################################################
class MovimentoCaixaMixin(object):

    def adicionar_novo_movimento_caixa(self, lancamento, novo_movimento):
        if isinstance(lancamento, Entrada):
            novo_movimento.entradas = novo_movimento.entradas + lancamento.valor_liquido
            novo_movimento.saldo_final = novo_movimento.saldo_final + lancamento.valor_liquido
            novo_movimento.save()
            # Atualizar os saldos dos proximos movimentos
            for m in MovimentoCaixa.objects.filter(data_movimento__gt=novo_movimento.data_movimento):
                m.saldo_inicial = m.saldo_inicial + lancamento.valor_liquido
                m.saldo_final = m.saldo_final + lancamento.valor_liquido
                m.save()

        elif isinstance(lancamento, Saida):
            novo_movimento.saidas = novo_movimento.saidas + lancamento.valor_liquido
            novo_movimento.saldo_final = novo_movimento.saldo_final - lancamento.valor_liquido
            novo_movimento.save()
            # Atualizar os saldos dos proximos movimentos
            for m in MovimentoCaixa.objects.filter(data_movimento__gt=novo_movimento.data_movimento):
                m.saldo_inicial = m.saldo_inicial - lancamento.valor_liquido
                m.saldo_final = m.saldo_final - lancamento.valor_liquido
                m.save()

    def remover_valor_movimento_caixa(self, lancamento, movimento, valor):
        if isinstance(lancamento, Entrada):
            movimento.entradas = movimento.entradas - valor
            movimento.saldo_final = movimento.saldo_final - valor
            movimento.save()
            for m in MovimentoCaixa.objects.filter(data_movimento__gt=movimento.data_movimento):
                m.saldo_inicial = m.saldo_inicial - valor
                m.saldo_final = m.saldo_final - valor
                m.save()
        elif isinstance(lancamento, Saida):
            movimento.saidas = movimento.saidas - valor
            movimento.saldo_final = movimento.saldo_final + valor
            movimento.save()
            for m in MovimentoCaixa.objects.filter(data_movimento__gt=movimento.data_movimento):
                m.saldo_inicial = m.saldo_inicial + valor
                m.saldo_final = m.saldo_final + valor
                m.save()

    def adicionar_valor_movimento_caixa(self, lancamento, movimento, valor):
        if isinstance(lancamento, Entrada):
            movimento.entradas = movimento.entradas + valor
            movimento.saldo_final = movimento.saldo_final + valor
            movimento.save()
            for m in MovimentoCaixa.objects.filter(data_movimento__gt=movimento.data_movimento):
                m.saldo_inicial = m.saldo_inicial + valor
                m.saldo_final = m.saldo_final + valor
                m.save()
        elif isinstance(lancamento, Saida):
            movimento.saidas = movimento.saidas + valor
            movimento.saldo_final = movimento.saldo_final - valor
            movimento.save()
            for m in MovimentoCaixa.objects.filter(data_movimento__gt=movimento.data_movimento):
                m.saldo_inicial = m.saldo_inicial - valor
                m.saldo_final = m.saldo_final - valor
                m.save()
    def verificar_remocao_movimento(self, movimento):
        # Deletar Caso essa seja a unica transacao do movimento antigo
        if ((movimento.saldo_final == movimento.saldo_inicial) and (movimento.entradas == 0)):
            movimento.delete()

    def atualizar_saldos(self, movimento):
        try:
            ultimo_mvmt = MovimentoCaixa.objects.filter(
                data_movimento__lt=movimento.data_movimento).latest('data_movimento')
            movimento.saldo_inicial = ultimo_mvmt.saldo_final
            movimento.saldo_final = movimento.saldo_inicial
            movimento.save()
        except MovimentoCaixa.DoesNotExist:
            pass

class AdicionarLancamentoBaseView(CustomCreateView, MovimentoCaixaMixin):
    permission_codename = 'add_lancamento'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, descricao=self.object.descricao)

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = form_class()
        form.initial['data_pagamento'] = datetime.today().strftime('%d/%m/%Y')
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.object = None
        # Tirar . dos campos decimais
        req_post = request.POST.copy()
        for key in req_post:
            if ('valor' in key or
                'juros' in key or
                    'abatimento' in key):
                req_post[key] = req_post[key].replace('.', '')
        request.POST = req_post

        form_class = self.get_form_class()
        form = form_class(request.POST)

        if form.is_valid():
            self.object = form.save(commit=False)

            if self.object.movimentar_caixa:
                mvmt = None
                created = None
                if self.object.data_pagamento:
                    mvmt, created = MovimentoCaixa.objects.get_or_create(
                        data_movimento=self.object.data_pagamento)
                elif self.object.data_vencimento:
                    mvmt, created = MovimentoCaixa.objects.get_or_create(
                        data_movimento=self.object.data_vencimento)

                if mvmt:
                    if created:
                        self.atualizar_saldos(mvmt)

                    self.adicionar_novo_movimento_caixa(
                        lancamento=self.object, novo_movimento=mvmt)
                    mvmt.save()
                    self.object.movimento_caixa = mvmt

            self.object.save()
            return self.form_valid(form)

        return self.form_invalid(form)
class AdicionarContaPagarView(AdicionarLancamentoBaseView):
    form_class = ContaPagarForm
    template_name = "lancamento_add.html"
    success_url = reverse_lazy('financeiro:listacontapagarview')
    success_message = "Conta a pagar <b>%(descricao)s </b>adicionada com sucesso."

    def get_context_data(self, **kwargs):
        context = super(AdicionarContaPagarView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'ADICIONAR CONTA A PAGAR'
        context['return_url'] = reverse_lazy('financeiro:listacontapagarview')
        return context
class AdicionarContaReceberView(AdicionarLancamentoBaseView):
    form_class = ContaReceberForm
    template_name = "lancamento_add.html"
    success_url = reverse_lazy('financeiro:listacontareceberview')
    success_message = "Conta a receber <b>%(descricao)s </b>adicionada com sucesso."

    def get_context_data(self, **kwargs):
        context = super(AdicionarContaReceberView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'ADICIONAR CONTA A RECEBER'
        context['return_url'] = reverse_lazy(
            'financeiro:listacontareceberview')
        return context
class AdicionarEntradaView(AdicionarLancamentoBaseView):
    form_class = EntradaForm
    template_name = "lancamento_add.html"
    success_url = reverse_lazy('financeiro:listarecebimentosview')
    success_message = "Recebimento <b>%(descricao)s </b>adicionado com sucesso."

    def get_context_data(self, **kwargs):
        context = super(AdicionarEntradaView, self).get_context_data(**kwargs)
        context['title_complete'] = 'ADICIONAR RECEBIMENTO'
        context['return_url'] = reverse_lazy(
            'financeiro:listarecebimentosview')
        return context
class AdicionarSaidaView(AdicionarLancamentoBaseView):
    form_class = SaidaForm
    template_name = "lancamento_add.html"
    success_url = reverse_lazy('financeiro:listapagamentosview')
    success_message = "Pagamento <b>%(descricao)s </b>adicionado com sucesso."

    def get_context_data(self, **kwargs):
        context = super(AdicionarSaidaView, self).get_context_data(**kwargs)
        context['title_complete'] = 'ADICIONAR PAGAMENTO'
        context['return_url'] = reverse_lazy('financeiro:listapagamentosview')
        return context

class EditarLancamentoBaseView(CustomUpdateView, MovimentoCaixaMixin):
    permission_codename = 'change_lancamento'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, descricao=self.object.descricao)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = form_class(instance=self.object)
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        # Tirar . dos campos decimais
        req_post = request.POST.copy()
        for key in req_post:
            if ('valor' in key or
                'juros' in key or
                    'abatimento' in key):
                req_post[key] = req_post[key].replace('.', '')

        request.POST = req_post

        self.object = self.get_object()
        vliquido_previo = self.object.valor_liquido
        form_class = self.get_form_class()
        form = form_class(request.POST, instance=self.object)

        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.save()

            variacao_valor = self.object.valor_liquido - vliquido_previo

            if self.object.movimento_caixa:
                if self.object.movimentar_caixa:
                    mvmt = None
                    created = None
                    if self.object.data_pagamento:
                        mvmt, created = MovimentoCaixa.objects.get_or_create(
                            data_movimento=self.object.data_pagamento)
                    elif self.object.data_vencimento:
                        mvmt, created = MovimentoCaixa.objects.get_or_create(
                            data_movimento=self.object.data_vencimento)

                    # Inseriu uma data de pagamento ou vencimento
                    if mvmt:
                        # Caso seja o mesmo mvmt(mesmo id e data)
                        if mvmt.id == self.object.movimento_caixa.id:
                            self.adicionar_valor_movimento_caixa(
                                self.object, self.object.movimento_caixa, variacao_valor)

                        # Caso tenha mudado a data, criar outro objeto e checar
                        # se o antigo pode ser deletado
                        else:
                            self.remover_valor_movimento_caixa(
                                self.object, self.object.movimento_caixa, vliquido_previo)
                            if created:
                                self.atualizar_saldos(mvmt)
                            else:
                                mvmt.refresh_from_db()

                            self.adicionar_novo_movimento_caixa(
                                lancamento=self.object, novo_movimento=mvmt)
                            self.verificar_remocao_movimento(
                                self.object.movimento_caixa)

                            mvmt.save()
                            self.object.movimento_caixa = mvmt

                    # Nao inseriu(removeu) data de vencimento ou pagamento
                    else:
                        self.remover_valor_movimento_caixa(
                            self.object, self.object.movimento_caixa, vliquido_previo)
                        self.verificar_remocao_movimento(
                            self.object.movimento_caixa)
                        self.object.movimento_caixa = None

                # Retirou opcao de movimentar o caixa
                else:
                    self.remover_valor_movimento_caixa(
                        self.object, self.object.movimento_caixa, vliquido_previo)
                    self.verificar_remocao_movimento(
                        self.object.movimento_caixa)
                    self.object.movimento_caixa = None

            # Nao possui movimento de caixa previo
            else:
                # Decide movimentar o caixa
                if self.object.movimentar_caixa:
                    mvmt = None
                    created = None
                    if self.object.data_pagamento:
                        mvmt, created = MovimentoCaixa.objects.get_or_create(
                            data_movimento=self.object.data_pagamento)
                    elif self.object.data_vencimento:
                        mvmt, created = MovimentoCaixa.objects.get_or_create(
                            data_movimento=self.object.data_vencimento)

                    if mvmt:
                        if created:
                            self.atualizar_saldos(mvmt)

                        self.adicionar_novo_movimento_caixa(
                            lancamento=self.object, novo_movimento=mvmt)
                        mvmt.save()
                        self.object.movimento_caixa = mvmt

            self.object.save()
            return self.form_valid(form)
        return self.form_invalid(form)
    
class EditarContaPagarView(EditarLancamentoBaseView):
    form_class = ContaPagarForm
    model = Saida
    template_name = "lancamento_edit.html"
    success_url = reverse_lazy('financeiro:listacontapagarview')
    success_message = "Conta a pagar <b>%(descricao)s </b>editada com sucesso."

    def get_context_data(self, **kwargs):
        context = super(EditarContaPagarView, self).get_context_data(**kwargs)
        context['return_url'] = reverse_lazy('financeiro:listacontapagarview')
        return context


class EditarContaReceberView(EditarLancamentoBaseView):
    form_class = ContaReceberForm
    model = Entrada
    template_name = "lancamento_edit.html"
    success_url = reverse_lazy('financeiro:listacontareceberview')
    success_message = "Conta a receber <b>%(descricao)s </b>editada com sucesso."

    def get_context_data(self, **kwargs):
        context = super(EditarContaReceberView,
                        self).get_context_data(**kwargs)
        context['return_url'] = reverse_lazy(
            'financeiro:listacontareceberview')
        return context
    
class EditarEntradaView(EditarLancamentoBaseView):
    form_class = EntradaForm
    model = Entrada
    template_name = "lancamento_edit.html"
    success_url = reverse_lazy('financeiro:listarecebimentosview')
    success_message = "Recebimento <b>%(descricao)s </b>editado com sucesso."

    def get_context_data(self, **kwargs):
        context = super(EditarEntradaView, self).get_context_data(**kwargs)
        context['return_url'] = reverse_lazy(
            'financeiro:listarecebimentosview')
        return context


class EditarSaidaView(EditarLancamentoBaseView):
    form_class = SaidaForm
    model = Saida
    template_name = "lancamento_edit.html"
    success_url = reverse_lazy('financeiro:listapagamentosview')
    success_message = "Pagamento <b>%(descricao)s </b>editado com sucesso."

    def get_context_data(self, **kwargs):
        context = super(EditarSaidaView, self).get_context_data(**kwargs)
        context['return_url'] = reverse_lazy('financeiro:listapagamentosview')
        return context

class LancamentoListBaseView(CustomListView, MovimentoCaixaMixin):
    permission_codename = 'view_lancamento'

    def get_queryset(self, object, status):
        return object.objects.filter(status__in=status)

    # Remover items selecionados da database
    def post(self, request, *args, **kwargs):
        if self.check_user_delete_permission(request, Lancamento):
            for key, value in request.POST.items():
                if value == "on":
                    instance = self.model.objects.get(id=key)
                    if(instance.movimento_caixa):
                        self.remover_valor_movimento_caixa(
                            instance, instance.movimento_caixa, instance.valor_liquido)
                        self.verificar_remocao_movimento(
                            instance.movimento_caixa)
                    instance.delete()
        return redirect(self.success_url)
    
class LancamentoListView(LancamentoListBaseView):
    template_name = 'lancamento_list.html'
    context_object_name = 'all_lancamentos'
    success_url = reverse_lazy('financeiro:listalancamentoview')

    def get_context_data(self, **kwargs):
        context = super(LancamentoListView, self).get_context_data(**kwargs)
        context['title_complete'] = 'TODOS OS LANÇAMENTOS'
        context['all_lancamentos_saidas'] = Saida.objects.all()
        return context

    def get_queryset(self):
        all_entradas = Entrada.objects.all()
        all_saidas = Saida.objects.all()
        all_lancamentos = list(chain(all_saidas, all_entradas))
        return all_lancamentos

    def post(self, request, *args, **kwargs):
        if self.check_user_delete_permission(request, Lancamento):
            for key, value in request.POST.items():
                if value == "on":
                    if Entrada.objects.filter(id=key).exists():
                        instance = Entrada.objects.get(id=key)
                    elif Saida.objects.filter(id=key).exists():
                        instance = Saida.objects.get(id=key)
                    else:
                        raise ValueError(
                            'Entrada/Saida para o lancamento escolhido nao existe.')
                    if(instance.movimento_caixa):
                        self.remover_valor_movimento_caixa(
                            instance, instance.movimento_caixa, instance.valor_liquido)
                        self.verificar_remocao_movimento(
                            instance.movimento_caixa)
                    instance.delete()
        return redirect(self.success_url)
    
class ContaPagarListView(LancamentoListBaseView):
    template_name = 'lancamento_list.html'
    model = Saida
    context_object_name = 'all_contaspagar'
    success_url = reverse_lazy('financeiro:listacontapagarview')

    def get_context_data(self, **kwargs):
        context = super(ContaPagarListView, self).get_context_data(**kwargs)
        context['title_complete'] = 'CONTAS A PAGAR'
        context['add_url'] = reverse_lazy('financeiro:addcontapagarview')
        return context

    def get_queryset(self):
        return super(ContaPagarListView, self).get_queryset(object=Saida, status=['1', '2'])


class ContaPagarAtrasadasListView(LancamentoListBaseView):
    template_name = 'lancamento_list.html'
    model = Saida
    context_object_name = 'all_contaspagar'
    success_url = reverse_lazy('financeiro:listacontapagaratrasadasview')

    def get_context_data(self, **kwargs):
        context = super(ContaPagarAtrasadasListView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'CONTAS A PAGAR ATRASADAS'
        context['add_url'] = reverse_lazy('financeiro:addcontapagarview')
        return context

    def get_queryset(self):
        return Saida.objects.filter(data_vencimento__lt=datetime.now().date(), status__in=['1', '2'])
    
class ContaPagarHojeListView(ContaPagarAtrasadasListView):
    success_url = reverse_lazy('financeiro:listacontapagarhojeview')

    def get_context_data(self, **kwargs):
        context = super(ContaPagarHojeListView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'CONTAS A PAGAR DO DIA ' + \
            datetime.now().date().strftime('%d/%m/%Y')
        context['add_url'] = reverse_lazy('financeiro:addcontapagarview')
        return context

    def get_queryset(self):
        return Saida.objects.filter(data_vencimento=datetime.now().date(), status__in=['1', '2'])


class ContaReceberListView(LancamentoListBaseView):
    template_name = 'lancamento_list.html'
    model = Entrada
    context_object_name = 'all_contasreceber'
    success_url = reverse_lazy('financeiro:listacontareceberview')

    def get_context_data(self, **kwargs):
        context = super(ContaReceberListView, self).get_context_data(**kwargs)
        context['title_complete'] = 'CONTAS A RECEBER'
        context['add_url'] = reverse_lazy('financeiro:addcontareceberview')
        return context

    def get_queryset(self):
        return super(ContaReceberListView, self).get_queryset(object=Entrada, status=['1', '2'])
    
class ContaReceberAtrasadasListView(LancamentoListBaseView):
    template_name = 'lancamento_list.html'
    model = Entrada
    context_object_name = 'all_contasreceber'
    success_url = reverse_lazy('financeiro:listacontareceberatrasadasview')

    def get_context_data(self, **kwargs):
        context = super(ContaReceberAtrasadasListView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'CONTAS A RECEBER ATRASADAS'
        context['add_url'] = reverse_lazy('financeiro:addcontareceberview')
        return context

    def get_queryset(self):
        return Entrada.objects.filter(data_vencimento__lt=datetime.now().date(), status__in=['1', '2'])


class ContaReceberHojeListView(ContaReceberAtrasadasListView):
    success_url = reverse_lazy('financeiro:listacontareceberhojeview')

    def get_context_data(self, **kwargs):
        context = super(ContaReceberHojeListView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'CONTAS A RECEBER DO DIA ' + \
            datetime.now().date().strftime('%d/%m/%Y')
        context['add_url'] = reverse_lazy('financeiro:addcontareceberview')
        return context

    def get_queryset(self):
        return Entrada.objects.filter(data_vencimento=datetime.now().date(), status__in=['1', '2'])
    
class EntradaListView(LancamentoListBaseView):
    template_name = 'lancamento_list.html'
    model = Entrada
    context_object_name = 'all_entradas'
    success_url = reverse_lazy('financeiro:listarecebimentosview')

    def get_context_data(self, **kwargs):
        context = super(EntradaListView, self).get_context_data(**kwargs)
        context['title_complete'] = 'RECEBIMENTOS'
        context['add_url'] = reverse_lazy('financeiro:addrecebimentoview')
        return context

    def get_queryset(self):
        return super(EntradaListView, self).get_queryset(object=Entrada, status=['0', ])


class SaidaListView(LancamentoListBaseView):
    template_name = 'lancamento_list.html'
    model = Saida
    context_object_name = 'all_saidas'
    success_url = reverse_lazy('financeiro:listapagamentosview')

    def get_context_data(self, **kwargs):
        context = super(SaidaListView, self).get_context_data(**kwargs)
        context['title_complete'] = 'PAGAMENTOS'
        context['add_url'] = reverse_lazy('financeiro:addpagamentoview')
        return context

    def get_queryset(self):
        return super(SaidaListView, self).get_queryset(object=Saida, status=['0', ])
    
class GerarLancamentoView(CustomView, MovimentoCaixaMixin):
    permission_codename = ['add_lancamento', 'change_lancamento']

    def post(self, request, *args, **kwargs):
        conta_id = request.POST['contaId']
        data = {}

        # Tipo conta: 0 = Receber, 1 = Pagar
        if request.POST['tipoConta'] == '0':
            obj = Entrada.objects.get(id=conta_id)
            data['url'] = reverse_lazy(
                'financeiro:editarrecebimentoview', kwargs={'pk': obj.id})
            obj.status = '0'
            obj.data_pagamento = datetime.strptime(
                request.POST['dataPagamento'], '%d/%m/%Y').strftime('%Y-%m-%d')
            obj.save()
            if obj.movimentar_caixa:
                self.atualizar_movimento_caixa(obj)
        elif request.POST['tipoConta'] == '1':
            obj = Saida.objects.get(id=conta_id)
            data['url'] = reverse_lazy(
                'financeiro:editarpagamentoview', kwargs={'pk': obj.id})
            obj.status = '0'
            obj.data_pagamento = datetime.strptime(
                request.POST['dataPagamento'], '%d/%m/%Y').strftime('%Y-%m-%d')
            obj.save()
            if obj.movimentar_caixa:
                self.atualizar_movimento_caixa(obj)

        return JsonResponse(data)

    def atualizar_movimento_caixa(self, object):
        mvmt = None
        created = None
        if object.data_pagamento:
            mvmt, created = MovimentoCaixa.objects.get_or_create(
                data_movimento=object.data_pagamento)

        if mvmt:
            # Caso a data esteja trocada
            if mvmt.id != object.movimento_caixa.id:
                # Atualizar os valores sem o movimento antigo
                self.remover_valor_movimento_caixa(
                    object, object.movimento_caixa, object.valor_liquido)
                if created:
                    self.atualizar_saldos(mvmt)
                else:
                    mvmt.refresh_from_db()

                self.verificar_remocao_movimento(object.movimento_caixa)
                self.adicionar_novo_movimento_caixa(
                    lancamento=object, novo_movimento=mvmt)

                mvmt.save()
                object.movimento_caixa = mvmt
                object.save()

class FluxoCaixaView(CustomListView):
    template_name = "fluxo.html"
    success_url = reverse_lazy('financeiro:fluxodecaixaview')
    context_object_name = 'movimentos'
    permission_codename = 'acesso_fluxodecaixa'

    def get_queryset(self):
   
        try:
            data_inicial = self.request.GET.get('from')
            data_final = self.request.GET.get('to')

            if data_inicial and data_final:
                data_inicial = datetime.strptime(data_inicial, '%d/%m/%Y')
                data_final = datetime.strptime(data_final, '%d/%m/%Y')
            elif data_inicial:
                data_inicial = datetime.strptime(data_inicial, '%d/%m/%Y')
                data_final = data_inicial
            elif data_final:
                data_final = datetime.strptime(data_final, '%d/%m/%Y')
                data_inicial = data_final
            else:
                data_inicial = datetime.now().replace(day=1).strftime('%Y-%m-%d')
                ultimo_dia_mes = calendar.monthrange(date.today().year, date.today().month)[1]
                data_final = datetime.now().replace(day=ultimo_dia_mes).strftime('%Y-%m-%d')

        except ValueError:
            data_inicial = datetime.now().replace(day=1).strftime('%Y-%m-%d')
            ultimo_dia_mes = calendar.monthrange(date.today().year, date.today().month)[1]
            data_final = datetime.now().replace(day=ultimo_dia_mes).strftime('%Y-%m-%d')
            messages.error(
                self.request, 'Formato de data incorreto, deve ser no formato DD/MM/AAAA')

        return MovimentoCaixa.objects.filter(data_movimento__range=(data_inicial, data_final))