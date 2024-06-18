# -*- coding: utf-8 -*-

from django.urls import reverse_lazy
from django.db.models import F

from core.custom_views import CustomCreateView, CustomListView, CustomUpdateView
from cadastro.forms.geral import ContratoForm, AreaForm, SolicitanteForm, AprovadorForm, ItemBmForm
from cadastro.forms.inline_formsets import EtapaAprovacaoFormSet
from cadastro.models.geral import Contrato, Area, Solicitante, Aprovador, EtapaAprovacao, ItemBm
from django.contrib import messages
from datetime import datetime

class AdicionarDocumentoView(CustomCreateView):
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.pk)
    def get_context_data(self, **kwargs):
        context = super(AdicionarDocumentoView, self).get_context_data(**kwargs)
        return self.view_context(context)
    def get(self, request, form_class, *args, **kwargs):
        self.object = None
        form = self.get_form(form_class)
        etapa_aprovacao_form = EtapaAprovacaoFormSet(prefix='etapa_aprovacao_form')
        return self.render_to_response(self.get_context_data(form=form,etapa_aprovacao_form=etapa_aprovacao_form,))                                                                                                                    
    def post(self, request, form_class, *args, **kwargs):
        self.object = None
        form = self.get_form(form_class)
        etapa_aprovacao_form = EtapaAprovacaoFormSet(request.POST, prefix='etapa_aprovacao_form')
        if (form.is_valid() and etapa_aprovacao_form.is_valid()):
            self.object = form.save(commit=False)
            self.object.save()
            etapa_aprovacao_form.instance = self.object
            etapa_aprovacao_form.save()
            return self.form_valid(form)
        return self.form_invalid(form=form,etapa_aprovacao_form=etapa_aprovacao_form)
                                 
class AdicionarAprovadorView(AdicionarDocumentoView):
    form_class = AprovadorForm
    template_name = "pessoa_add.html"
    success_url = reverse_lazy('cadastro:listaaprovadorview')
    success_message = "<b>Aprovador %(id)s </b>adicionado com sucesso."
    permission_codename = 'add_aprovador'
    def view_context(self, context):
        context['title_complete'] = 'ADICIONAR APROVADOR'
        context['return_url'] = reverse_lazy('cadastro:listaaprovadorview')
        context['tipo_pessoa'] = 'aprovador'
        return context
    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(AdicionarAprovadorView, self).get(request, form_class, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(AdicionarAprovadorView, self).post(request, form_class, *args, **kwargs)
class EditarDocumentoView(CustomUpdateView):
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.pk)
    def get_context_data(self, **kwargs):
        context = super(EditarDocumentoView, self).get_context_data(**kwargs)
        return self.view_context(context)
    def get(self, request, form_class, *args, **kwargs):
        form = self.get_form(form_class)
        etapa_aprovacao_form = EtapaAprovacaoFormSet(
            instance=self.object, prefix='etapa_aprovacao_form')
        if EtapaAprovacao.objects.filter(aprovador=self.object.pk).count():
            etapa_aprovacao_form.extra = 0
        return self.render_to_response(self.get_context_data(form=form, etapa_aprovacao_form=etapa_aprovacao_form))
    def post(self, request, form_class, *args, **kwargs):
        form = self.get_form(form_class)
        etapa_aprovacao_form = EtapaAprovacaoFormSet(
            request.POST, prefix='etapa_aprovacao_form', instance=self.object)
        if (form.is_valid() and etapa_aprovacao_form.is_valid()):
            self.object = form.save(commit=False)
            self.object.save()
            etapa_aprovacao_form.instance = self.object
            etapa_aprovacao_form.save()
            return self.form_valid(form)
        return self.form_invalid(form=form,etapa_aprovacao_form=etapa_aprovacao_form,)
                                 
class EditarAprovadorView(EditarDocumentoView):
    form_class = AprovadorForm
    model = Aprovador
    template_name = "pessoa_edit.html"
    success_url = reverse_lazy('cadastro:listaaprovadorview')
    success_message = "<b>Aprovador %(id)s </b>editado com sucesso."
    permission_codename = 'change_aprovador'
    def view_context(self, context):
        context['title_complete'] = 'EDITAR APROVADOR'
        context['return_url'] = reverse_lazy('cadastro:listaaprovadorview')
        context['tipo_pessoa'] = 'aprovador'
        return context
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        return super(EditarAprovadorView, self).get(request, form_class, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        return super(EditarAprovadorView, self).post(request, form_class, *args, **kwargs)
    
class DocumentoListView(CustomListView):
    def get_context_data(self, **kwargs):
        context = super(DocumentoListView, self).get_context_data(**kwargs)
        return self.view_context(context)
class AprovadorListView(DocumentoListView):
    template_name = 'pessoa_list.html'
    model = Aprovador
    context_object_name = 'all_aprovadors'
    success_url = reverse_lazy('cadastro:listaaprovadorview')
    permission_codename = 'view_aprovador'
    def view_context(self, context):
        context['title_complete'] = 'APROVADORES'
        context['add_url'] = reverse_lazy('cadastro:addaprovadorview')
        context['tipo_pessoa'] = 'aprovador'
        return context


############## pop up views
class AdicionarOutrosBaseView(CustomCreateView):
    template_name = "popup_form.html"
    def get_context_data(self, **kwargs):
        context = super(AdicionarOutrosBaseView,
                        self).get_context_data(**kwargs)
        context['titulo'] = 'Adicionar ' + self.model.__name__
        return context
class EditarOutrosBaseView(CustomUpdateView):
    template_name = "popup_form.html"
    def get_context_data(self, **kwargs):
        context = super(EditarOutrosBaseView,
                        self).get_context_data(**kwargs)
        context['titulo'] = 'Editar {0}: {1}'.format(
            self.model.__name__, str(self.object))
        return context

class AdicionarContratoView(AdicionarOutrosBaseView):
    form_class = ContratoForm
    model = Contrato
    success_url = reverse_lazy('cadastro:addcontratoview')
    permission_codename = 'add_contrato'
class ContratosListView(CustomListView):
    model = Contrato
    template_name = 'geral/contrato_list.html'
    context_object_name = 'all_contratos'
    success_url = reverse_lazy('cadastro:listacontratosview')
    permission_codename = 'view_contrato'
class EditarContratoView(EditarOutrosBaseView):
    form_class = ContratoForm
    model = Contrato
    success_url = reverse_lazy('cadastro:listacontratosview')
    permission_codename = 'change_contrato'

class AdicionarAreaView(AdicionarOutrosBaseView):
    form_class = AreaForm
    model = Area
    success_url = reverse_lazy('cadastro:addareaview')
    permission_codename = 'add_area'
class AreasListView(CustomListView):
    model = Area
    template_name = 'geral/area_list.html'
    context_object_name = 'all_areas'
    success_url = reverse_lazy('cadastro:listaareasview')
    permission_codename = 'view_area'
class EditarAreaView(EditarOutrosBaseView):
    form_class = AreaForm
    model = Area
    success_url = reverse_lazy('cadastro:listaareasview')
    permission_codename = 'change_area'

class AdicionarSolicitanteView(AdicionarOutrosBaseView):
    form_class = SolicitanteForm
    model = Solicitante
    success_url = reverse_lazy('cadastro:addsolicitanteview')
    permission_codename = 'add_solicitante'
class SolicitantesListView(CustomListView):
    model = Solicitante
    template_name = 'geral/solicitante_list.html'
    context_object_name = 'all_solicitantes'
    success_url = reverse_lazy('cadastro:listasolicitantesview')
    permission_codename = 'view_solicitante'
class EditarSolicitanteView(EditarOutrosBaseView):
    form_class = SolicitanteForm
    model = Solicitante
    success_url = reverse_lazy('cadastro:listasolicitantesview')
    permission_codename = 'change_solicitante'

class AdicionarItemBmView(AdicionarOutrosBaseView):
    form_class = ItemBmForm
    model = ItemBm
    success_url = reverse_lazy('cadastro:additemmedview')
    permission_codename = 'add_itemmed'
class ItemBmListView(CustomListView):
    model = ItemBm
    template_name = 'geral/itensmed_list.html'
    context_object_name = 'all_itensmed'
    success_url = reverse_lazy('cadastro:listaitensmedview')
    permission_codename = 'view_itemmed'
    def get_queryset(self):
        try:
            filtro = self.request.GET.get('item_filtro')
            if filtro:
                filtro = self.request.GET.get('item_filtro')
            else:
                filtro = '10-100'
        except ValueError:
            messages.error(
                self.request, 'FILTRO NÃO VÁLIDO')
        return ItemBm.objects.filter(item_ref__icontains=filtro)


class EditarItemBmView(EditarOutrosBaseView):
    form_class = ItemBmForm
    model = ItemBm
    success_url = reverse_lazy('cadastro:listaitensmedview')
    permission_codename = 'change_itemmed'