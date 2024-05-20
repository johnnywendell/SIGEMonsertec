# -*- coding: utf-8 -*-

from django.urls import reverse_lazy
from django.db.models import F
from core.custom_views import CustomCreateView, CustomListView, CustomUpdateView
from .forms import RDOForm, ASForm, ItemFormSet
from .models import RDO, AS, ItemMedicao

class AdicionarDocumentoView(CustomCreateView):
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.pk)
    def get_context_data(self, **kwargs):
        context = super(AdicionarDocumentoView, self).get_context_data(**kwargs)
        return self.view_context(context)
    def get(self, request, form_class, *args, **kwargs):
        self.object = None
        form = self.get_form(form_class)
        item_form = ItemFormSet(prefix='item_form')
        return self.render_to_response(self.get_context_data(form=form,item_form=item_form,))                                                                                                                    
    def post(self, request, form_class, *args, **kwargs):
        self.object = None
        form = self.get_form(form_class)
        item_form = ItemFormSet(request.POST, prefix='item_form')
        if (form.is_valid() and item_form.is_valid()):
            self.object = form.save(commit=False)
            self.object.criado_por = self.request.user
            self.object.save()
            item_form.instance = self.object
            item_form.save()
            return self.form_valid(form)
        return self.form_invalid(form=form,item_form=item_form)
                                 
class AdicionarRDOView(AdicionarDocumentoView):
    form_class = RDOForm
    template_name = "pessoa_add.html"
    success_url = reverse_lazy('planejamento:listardoview')
    success_message = "<b>rdo %(id)s </b>adicionado com sucesso."
    permission_codename = 'add_rdo'
    def view_context(self, context):
        context['title_complete'] = 'ADICIONAR RDO'
        context['return_url'] = reverse_lazy('planejamento:listardoview')
        context['tipo_pessoa'] = 'rdo'
        return context
    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(AdicionarRDOView, self).get(request, form_class, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(AdicionarRDOView, self).post(request, form_class, *args, **kwargs)
    
class EditarDocumentoView(CustomUpdateView):
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.pk)
    def get_context_data(self, **kwargs):
        context = super(EditarDocumentoView, self).get_context_data(**kwargs)
        return self.view_context(context)
    def get(self, request, form_class, *args, **kwargs):
        form = self.get_form(form_class)
        item_form = ItemFormSet(
            instance=self.object, prefix='item_form')
        if ItemMedicao.objects.filter(rdo=self.object.pk).count():
            item_form.extra = 0
        return self.render_to_response(self.get_context_data(form=form, item_form=item_form))
    def post(self, request, form_class, *args, **kwargs):
        form = self.get_form(form_class)
        item_form = ItemFormSet(
            request.POST, prefix='item_form', instance=self.object)
        if (form.is_valid() and item_form.is_valid()):
            self.object = form.save(commit=False)
            self.object.save()
            item_form.instance = self.object
            item_form.save()
            return self.form_valid(form)
        return self.form_invalid(form=form,item_form=item_form,)
                                 
class EditarRDOView(EditarDocumentoView):
    form_class = RDOForm
    model = RDO
    template_name = "pessoa_edit.html"
    success_url = reverse_lazy('planejamento:listardoview')
    success_message = "<b>rdo %(id)s </b>editado com sucesso."
    permission_codename = 'change_rdo'
    def view_context(self, context):
        context['title_complete'] = 'EDITAR RDO'
        context['return_url'] = reverse_lazy('planejamento:listardoview')
        context['tipo_pessoa'] = 'rdo'
        return context
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        return super(EditarRDOView, self).get(request, form_class, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        return super(EditarRDOView, self).post(request, form_class, *args, **kwargs)
    
class DocumentoListView(CustomListView):
    def get_context_data(self, **kwargs):
        context = super(DocumentoListView, self).get_context_data(**kwargs)
        return self.view_context(context)
class RDOListView(DocumentoListView):
    template_name = 'pessoa_list.html'
    model = RDO
    context_object_name = 'all_rdos'
    success_url = reverse_lazy('planejamento:listardoview')
    permission_codename = 'view_rdo'
    def view_context(self, context):
        context['title_complete'] = "RDO's"
        context['add_url'] = reverse_lazy('planejamento:addrdoview')
        context['tipo_pessoa'] = 'rdo'
        return context
