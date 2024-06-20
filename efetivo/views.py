from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import F
from django.http import HttpResponse
from core.custom_views import CustomCreateView, CustomListView, CustomUpdateView, CustomView
from django.views.generic import TemplateView
from .forms import ColaboradorForm,ApontamentoForm,ApontamentoColaboradorFormSet
from .models import Colaborador, Apontamento,ApontamentoColaborador
from datetime import datetime
import xlwt

#################pop up###############

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

class AdicionarColaboradorView(AdicionarOutrosBaseView):
    form_class = ColaboradorForm
    model = Colaborador
    success_url = reverse_lazy('efetivo:addcolaboradorview')
    permission_codename = 'add_colaborador'
class ColaboradorListView(CustomListView):
    model = Colaborador
    template_name = 'colaborador_list.html'
    context_object_name = 'all_colaboradores'
    success_url = reverse_lazy('efetivo:listacolaboradoreview')
    permission_codename = 'view_colaborador'
class EditarColaboradorView(EditarOutrosBaseView):
    form_class = ColaboradorForm
    model = Colaborador
    success_url = reverse_lazy('efetivo:listacolaboradoreview')
    permission_codename = 'change_colaborador'


class ExportarView(TemplateView):
    template_name = 'exportar_apontamentos.html'
    permission_codename = 'view_colaborador'

###################### detalhada#############
class AdicionarDocumentoView(CustomCreateView):
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.pk)
    def get_context_data(self, **kwargs):
        context = super(AdicionarDocumentoView, self).get_context_data(**kwargs)
        return self.view_context(context)
    def get(self, request, form_class, *args, **kwargs):
        self.object = None
        form = self.get_form(form_class)
        apontamento_form = ApontamentoColaboradorFormSet(prefix='apontamento_form')
        return self.render_to_response(self.get_context_data(form=form,
                                                             apontamento_form=apontamento_form,))                                                            
    def post(self, request, form_class, *args, **kwargs):
        self.object = None
        req_post = request.POST.copy()
        request.POST = req_post
        form = self.get_form(form_class)
        apontamento_form = ApontamentoColaboradorFormSet(request.POST, prefix='apontamento_form')
        if (form.is_valid() and apontamento_form.is_valid()):
            self.object = form.save(commit=False)
            self.object.criado_por = self.request.user
            self.object.save()
            apontamento_form.instance = self.object
            apontamento_form.save()
            return self.form_valid(form)
        return self.form_invalid(form=form,
                                 apontamento_form=apontamento_form,
                                 )

class AdicionarApontamentoView(AdicionarDocumentoView):
    form_class = ApontamentoForm
    template_name = "pessoa_add.html"
    success_url = reverse_lazy('efetivo:listaapontamentoview')
    success_message = "<b>Apontamento %(id)s </b>feito com sucesso."
    permission_codename = 'add_apontamento'
    def view_context(self, context):
        context['title_complete'] = 'ADICIONAR APONTAMENTO'
        context['return_url'] = reverse_lazy('efetivo:listaapontamentoview')
        context['tipo_pessoa'] = 'apontamento'
        return context
    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(AdicionarApontamentoView, self).get(request, form_class, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(AdicionarApontamentoView, self).post(request, form_class, *args, **kwargs)
    
class DocumentoListView(CustomListView):
    def get_context_data(self, **kwargs):
        context = super(DocumentoListView, self).get_context_data(**kwargs)
        return self.view_context(context)

class ApontamentoListView(DocumentoListView):
    template_name = 'pessoa_list.html'
    model = Apontamento
    context_object_name = 'all_apontamentos'
    success_url = reverse_lazy('efetivo:listaapontamentoview')
    permission_codename = 'view_apontamento'
    def view_context(self, context):
        context['title_complete'] = 'APONTAMENTOS'
        context['add_url'] = reverse_lazy('efetivo:addapontamentoview')
        context['tipo_pessoa'] = 'apontamento'
        return context
    def get_queryset(self):
        user = self.request.user
        is_superadmin = user.is_superuser
        is_staff = user.is_staff 
        if is_superadmin or is_staff:
            queryset = super().get_queryset()
        else:
            queryset = super().get_queryset().filter(criado_por=user)
        return queryset

class EditarDocumentoView(CustomUpdateView):
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.pk)
    def get_context_data(self, **kwargs):
        context = super(EditarDocumentoView, self).get_context_data(**kwargs)
        return self.view_context(context)
    def get(self, request, form_class, *args, **kwargs):
        form = self.get_form(form_class)
        apontamento_form = ApontamentoColaboradorFormSet(
            instance=self.object, prefix='apontamento_form')
        if ApontamentoColaborador.objects.filter(apontamento=self.object.pk).count():
            apontamento_form.extra = 0
        return self.render_to_response(self.get_context_data(form=form, apontamento_form=apontamento_form))
    def post(self, request, form_class, *args, **kwargs):
        req_post = request.POST.copy()
        request.POST = req_post
        form = self.get_form(form_class)
        apontamento_form = ApontamentoColaboradorFormSet(
            request.POST, prefix='apontamento_form', instance=self.object)
        if (form.is_valid() and apontamento_form.is_valid()):
            self.object = form.save(commit=False)
            self.object.criado_por = self.request.user
            self.object.save()
            apontamento_form.instance = self.object
            apontamento_form.save()
            return self.form_valid(form)
        return self.form_invalid(form=form,
                                 apontamento_form=apontamento_form,)
    
class EditarApontamentoView(EditarDocumentoView):
    form_class = ApontamentoForm
    model = Apontamento
    template_name = "pessoa_edit.html"
    success_url = reverse_lazy('efetivo:listaapontamentoview')
    success_message = "<b>Apontamento %(id)s </b>editado com sucesso."
    permission_codename = 'change_apontamento'
    def view_context(self, context):
        context['title_complete'] = 'EDITAR APONTAMENTO N°' + \
            str(self.object.id)
        context['return_url'] = reverse_lazy('efetivo:listaapontamentoview')
        context['tipo_pessoa'] = 'apontamento'
        return context
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        return super(EditarApontamentoView, self).get(request, form_class, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        return super(EditarApontamentoView, self).post(request, form_class, *args, **kwargs)

############ CÓPIA LANÇAMENTO ########

class GerarCopiaEfetivoView(CustomView):
    def get(self, request, instance, redirect_url, *args, **kwargs):
        apontamentos = instance.apontamentos.all()
        print(apontamentos)
        instance.pk = None
        instance.id = None
        instance.data = datetime.now().date()
        instance.save()
        for item in apontamentos:
            item.pk = None
            item.id = None
            
            item.save()
            instance.apontamentos.add(item)
        return redirect(reverse_lazy(redirect_url, kwargs={'pk': instance.id}))
    
class GerarCopiaApontamentoView(GerarCopiaEfetivoView):
    permission_codename = 'add_apontamento'
    def get(self, request, *args, **kwargs):
        apontamento_id = kwargs.get('pk', None)
        instance = Apontamento.objects.get(id=apontamento_id)
        redirect_url = 'efetivo:editarapontamentoview'
        return super(GerarCopiaApontamentoView, self).get(request, instance, redirect_url, *args, **kwargs)


def export_xlsx(model, filename, queryset, columns):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(model)

    row_num = 0

    header_style = xlwt.easyxf('pattern: pattern solid, fore_color dark_blue; font: color white, bold True;')

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], header_style)

    default_style = xlwt.XFStyle()

    # Definindo um estilo para data (DD/MM/YYYY)
    date_style = xlwt.easyxf(num_format_str='DD/MM/YYYY')

    rows = queryset
    for row, rowdata in enumerate(rows):
        row_num += 1
        for col, val in enumerate(rowdata):
            if 'data' in columns[col].lower():
                default_style = date_style
            else:
                default_style = xlwt.XFStyle()  # Reseta o estilo para não afetar outras colunas
            ws.write(row_num, col, val, default_style)

    wb.save(response)
    return response

def export_efetivo_xls(request):
    MDATA = datetime.now().strftime('%Y-%m-%d')
    model = 'ApontamentoColaborador'
    filename = 'efetivo_monsertec.xls'
    _filename = filename.split('.')
    filename_final = f'{_filename[0]}_{MDATA}.{_filename[1]}'
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    queryset = ApontamentoColaborador.objects.filter(apontamento__data__range=[start_date, end_date]).values_list('apontamento__data',
            'colaborador__nome',
            'colaborador__matricula',
            'status',
            'apontamento__area__area',  
            'apontamento__projeto_cod__projeto_nome',
            'apontamento__disciplina',
            'lider')                                      
    columns = ('Data',
        'Nome',
        'Matricula',
        'Status',
        'Área',
        'Projeto Código',
        'Disciplina',
        'Líder')
                                                                     
    response = export_xlsx(model, filename_final, queryset, columns)
    return response
