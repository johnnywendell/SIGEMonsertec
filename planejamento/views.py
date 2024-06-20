# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import resolve_url,get_object_or_404
from django.urls import reverse_lazy
from django.db.models import F, FloatField
from core.custom_views import CustomCreateView, CustomListView, CustomUpdateView
from .forms import RDOForm, ASForm, ItemFormSet, ProjetoForm, BoletimMedicaoForm
from .models import RDO, AS, ItemMedicao, ProjetoCodigo, BoletimMedicao
from canteirojato.models import Material
from canteirojato.models import Romaneio
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models.functions import Coalesce

class AdicionarDocumentoView(CustomCreateView):
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.pk)
    def get_context_data(self, **kwargs):
        context = super(AdicionarDocumentoView, self).get_context_data(**kwargs)
        return self.view_context(context)
    def get(self, request, form_class, *args, **kwargs):
        self.object = None
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))                                                                                                                    
    def post(self, request, form_class, *args, **kwargs):
        self.object = None
        form = self.get_form(form_class)
        if (form.is_valid()):
            self.object = form.save(commit=False)
            self.object.criado_por = self.request.user
            self.object.save()
            return self.form_valid(form)
        return self.form_invalid(form=form)

class AdicionarBoletimMedicaoRDOView(AdicionarDocumentoView):
    form_class = BoletimMedicaoForm
    template_name = "pessoa_add.html"
    success_url = reverse_lazy('planejamento:listabmview')
    success_message = "<b>Boletim de medição %(id)s </b>adicionado com sucesso."
    permission_codename = 'add_boletimmedicao'
    def view_context(self, context):
        context['title_complete'] = 'ADICIONAR BOLETIM DE MEDIÇÃO'
        context['return_url'] = reverse_lazy('planejamento:listabmview')
        context['tipo_pessoa'] = 'boletimmedicao'
        return context
    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(AdicionarBoletimMedicaoRDOView, self).get(request, form_class, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(AdicionarBoletimMedicaoRDOView, self).post(request, form_class, *args, **kwargs)


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
        return self.render_to_response(self.get_context_data(form=form))
    def post(self, request, form_class, *args, **kwargs):
        form = self.get_form(form_class)
        if (form.is_valid()):
            self.object = form.save(commit=False)
            self.object.save()
            return self.form_valid(form)
        return self.form_invalid(form=form,)
                                 
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

class EditarBoletimMedicaoView(EditarDocumentoView):
    form_class = BoletimMedicaoForm
    model = BoletimMedicao
    template_name = "pessoa_edit.html"
    success_url = reverse_lazy('planejamento:listabmview')
    success_message = "<b>Boletim de medição %(id)s </b>editado com sucesso."
    permission_codename = 'change_boletimmedicao'
    def view_context(self, context):
        context['title_complete'] = 'EDITAR BOLETIM DE MEDIÇÃO'
        context['return_url'] = reverse_lazy('planejamento:listabmview')
        context['tipo_pessoa'] = 'boletimmedicao'
        romaneios_sem_medicao = Romaneio.objects.filter(bm__isnull=True)
        romaneios_da_medicao = Romaneio.objects.filter(bm=self.object.id)
        context['romaneios_sem_medicao'] = romaneios_sem_medicao
        context['romaneios_da_medicao'] = romaneios_da_medicao
        return context
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        return super(EditarBoletimMedicaoView, self).get(request, form_class, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        return super(EditarBoletimMedicaoView, self).post(request, form_class, *args, **kwargs)
def atualizar_romaneios_selecionados(request):
    if request.method == 'POST':
        vi = request.POST.get('valores_romaneios')
        id = request.POST.get('valores_id')
        vi = str(vi)
        present = vi.split(",")
        present.pop()
        for i in present:
            if not i == "null":
                Romaneio.objects.filter(pk=i).update(bm=id)
        url='planejamento:editarbmview'
        return HttpResponseRedirect(resolve_url(url,id))


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

class BoletimMedicaoListView(DocumentoListView):
    template_name = 'pessoa_list.html'
    model = BoletimMedicao
    context_object_name = 'all_bms'
    success_url = reverse_lazy('planejamento:listabmview')
    permission_codename = 'view_boletimmedicao'
    def view_context(self, context):
        context['title_complete'] = "BOLETIM DE MEDIÇÃO"
        context['add_url'] = reverse_lazy('planejamento:addbmview')
        context['tipo_pessoa'] = 'boletimmedicao'
        return context

########################## Pop up views #############################

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

class AdicionarProjetoView(AdicionarOutrosBaseView):
    form_class = ProjetoForm
    model = ProjetoCodigo
    success_url = reverse_lazy('planejamento:addprojetoview')
    permission_codename = 'add_projetocodigo'
class ProjetoListView(CustomListView):
    model = ProjetoCodigo
    template_name = 'projeto_list.html'
    context_object_name = 'all_projetos'
    success_url = reverse_lazy('planejamento:listaprojetoview')
    permission_codename = 'view_projetocodigo'
class EditarProjetoView(EditarOutrosBaseView):
    form_class = ProjetoForm
    model = ProjetoCodigo
    success_url = reverse_lazy('planejamento:listaprojetoview')
    permission_codename = 'change_projetocodigo'



############# PDF VIEWS ##############
from django.db.models import Sum, F, Q, Value
from django.db.models.functions import Concat

def render_pdf_view(request, pk):
    object = get_object_or_404(BoletimMedicao, pk=pk)
    template_path = 'bms/bm.html'
    ###loucura
    material_items = Material.objects.filter(n_romaneio__bm=pk).annotate(
    jato_ref=F('jato__item_ref'),
    tf_ref=F('tf__item_ref'),
    ti_ref=F('ti__item_ref'),
    ta_ref=F('ta__item_ref'),
    jato_descr=F('jato__descricao'),
    tf_descr=F('tf__descricao'),
    ti_descr=F('ti__descricao'),
    ta_descr=F('ta__descricao'),
    jato_und=F('jato__und'),
    tf_und=F('tf__und'),
    ti_und=F('ti__und'),
    ta_und=F('ta__und'),
    jato_preco=F('jato__preco_item'),
    tf_preco=F('tf__preco_item'),
    ti_preco=F('ti__preco_item'),
    ta_preco=F('ta__preco_item'),
    m2_sum=Sum('m2')
                    ).values(
                        'jato_ref', 'tf_ref', 'ti_ref', 'ta_ref',
                        'jato_descr', 'tf_descr', 'ti_descr', 'ta_descr',
                        'jato_und', 'tf_und', 'ti_und', 'ta_und',
                        'jato_preco', 'tf_preco', 'ti_preco', 'ta_preco',
                        'm2_sum'
                    )

    # Concatenar os resultados e somar os m2 para cada item_ref
    results = {}
    for item in material_items:
        for prefix in ['jato', 'tf', 'ti', 'ta']:
            item_ref = item[f'{prefix}_ref']
            if item_ref:
                if item_ref not in results:
                    results[item_ref] = {
                        'item_ref': item_ref,
                        'descricao': item[f'{prefix}_descr'],
                        'und': item[f'{prefix}_und'],
                        'preco_item': item[f'{prefix}_preco'],
                        'm2_sum': item['m2_sum'],
                        'valor': item[f'{prefix}_preco'] * item['m2_sum']
                    }
                else:
                    results[item_ref]['m2_sum'] += item['m2_sum']
                    results[item_ref]['valor'] += item[f'{prefix}_preco'] * item['m2_sum']
    # Converter o dicionário de resultados para uma lista
    final_results = list(results.values())
    ####
    total_material_items = Material.objects.filter(n_romaneio__bm=pk).annotate(
        jato_total=Coalesce(F('jato__preco_item') * F('m2'), 0.0, output_field=FloatField()),
        tf_total=Coalesce(F('tf__preco_item') * F('m2'), 0.0, output_field=FloatField()),
        ti_total=Coalesce(F('ti__preco_item') * F('m2'), 0.0, output_field=FloatField()),
        ta_total=Coalesce(F('ta__preco_item') * F('m2'), 0.0, output_field=FloatField())
    ).aggregate(
        total_value=Sum(F('jato_total') + F('tf_total') + F('ti_total') + F('ta_total'))
    )

    total_value = total_material_items['total_value']
    object.valor = format(total_value,'.3f')
    object.save()
    context = {'object': object, 'final_results':final_results}
   
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    #if download
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
