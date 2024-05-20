
from core.custom_views import CustomView, CustomCreateView, CustomListView, CustomUpdateView
from .forms import RelatorioAreaForm, RelatorioJatoForm, EtapaFormSet,PhotoForm
from .models import RelatorioArea, RelatorioJato, EtapaPintura, Photo, Relatorio
from canteirojato.models import Material
from django.urls import reverse_lazy
from django.shortcuts import redirect,get_object_or_404,resolve_url
from django.http import HttpResponse,  HttpResponseRedirect

from django.template.loader import get_template
from xhtml2pdf import pisa

class AdicionarDocumentoView(CustomCreateView):

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.pk)

    def get_context_data(self, **kwargs):
        context = super(AdicionarDocumentoView, self).get_context_data(**kwargs)
        return self.view_context(context)

    def get(self, request, form_class, *args, **kwargs):
        self.object = None

        form = self.get_form(form_class)
        etapa_form = EtapaFormSet(prefix='etapa_form')
    
        return self.render_to_response(self.get_context_data(form=form,
                                                             etapa_form=etapa_form,
                                                            ))
                                                             
    def post(self, request, form_class, *args, **kwargs):
        self.object = None

        form = self.get_form(form_class)
        etapa_form = EtapaFormSet(request.POST, prefix='etapa_form')
       

        if (form.is_valid() and etapa_form.is_valid()):
            self.object = form.save(commit=False)
            self.object.criado_por = self.request.user
            self.object.save()
            etapa_form.instance = self.object
            etapa_form.save()
          

            return self.form_valid(form)

        return self.form_invalid(form=form,
                                 etapa_form=etapa_form,)
               
                                 

class AdicionarRelatorioAreaView(AdicionarDocumentoView):
    form_class = RelatorioAreaForm
    template_name = "pessoa_add.html"
    success_url = reverse_lazy('qualidade:listarelatorioareaview')
    success_message = "<b>Relatório %(id)s </b>adicionado com sucesso."
    permission_codename = 'add_relatorioarea'

    def view_context(self, context):
        context['title_complete'] = 'ADICIONAR RELATÓRIO (ÁREA)'
        context['return_url'] = reverse_lazy('qualidade:listarelatorioareaview')
        context['tipo_pessoa'] = 'relatorioarea'
        return context

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(AdicionarRelatorioAreaView, self).get(request, form_class, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(AdicionarRelatorioAreaView, self).post(request, form_class, *args, **kwargs)

class AdicionarRelatorioJatoView(AdicionarDocumentoView):
    form_class = RelatorioJatoForm
    template_name = "pessoa_add.html"
    success_url = reverse_lazy('qualidade:listarelatoriojatoview')
    success_message = "<b>Relatório %(id)s </b>adicionado com sucesso."
    permission_codename = 'add_relatoriojato'

    def view_context(self, context):
        context['title_complete'] = 'ADICIONAR RELATÓRIO (CANTEIRO DE JATO)'
        context['return_url'] = reverse_lazy('qualidade:listarelatoriojatoview')
        context['tipo_pessoa'] = 'relatoriojato'
        return context

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(AdicionarRelatorioJatoView, self).get(request, form_class, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(AdicionarRelatorioJatoView, self).post(request, form_class, *args, **kwargs)

class DocumentoListView(CustomListView):
    def get_context_data(self, **kwargs):
        context = super(DocumentoListView, self).get_context_data(**kwargs)
        return self.view_context(context)

class RelatorioAreaListView(DocumentoListView):
    template_name = 'pessoa_list.html'
    model = RelatorioArea
    context_object_name = 'all_relatorios_area'
    success_url = reverse_lazy('qualidade:listarelatorioareaview')
    permission_codename = 'view_relatorio_area'

    def view_context(self, context):
        context['title_complete'] = 'RELATÓRIOS (ÁREA)'
        context['add_url'] = reverse_lazy('qualidade:addrelatorioareaview')
        context['tipo_pessoa'] = 'relatorioarea'
        return context
    
class RelatorioJatoListView(DocumentoListView):
    template_name = 'pessoa_list.html'
    model = RelatorioJato
    context_object_name = 'all_relatorios_area'
    success_url = reverse_lazy('qualidade:listarelatoriojatoview')
    permission_codename = 'view_relatorio_jato'

    def view_context(self, context):
        context['title_complete'] = 'RELATÓRIOS (CANTEIRO DE JATO)'
        context['add_url'] = reverse_lazy('qualidade:addrelatoriojatoview')
        context['tipo_pessoa'] = 'relatoriojato'
        return context
    

class EditarDocumentoView(CustomUpdateView):

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.pk)

    def get_context_data(self, **kwargs):
        context = super(EditarDocumentoView, self).get_context_data(**kwargs)
        return self.view_context(context)

    def get(self, request, form_class, *args, **kwargs):

        form = self.get_form(form_class)

        etapa_form = EtapaFormSet(
            instance=self.object, prefix='etapa_form')

        if EtapaPintura.objects.filter(rip_n=self.object.pk).count():
            etapa_form.extra = 0

        return self.render_to_response(self.get_context_data(form=form, etapa_form=etapa_form,))

    def post(self, request, form_class, *args, **kwargs):

        form = self.get_form(form_class)
        etapa_form = EtapaFormSet(
            request.POST, prefix='etapa_form', instance=self.object)

        if (form.is_valid() and etapa_form.is_valid()):
            self.object = form.save(commit=False)
            self.object.criado_por = self.request.user
            self.object.save()

            etapa_form.instance = self.object
            etapa_form.save()

            return self.form_valid(form)

        return self.form_invalid(form=form,
                                 etapa_form=etapa_form,)
    
class EditarRelatorioAreaView(EditarDocumentoView):
    form_class = RelatorioAreaForm
    model = RelatorioArea
    template_name = "pessoa_edit.html"
    success_url = reverse_lazy('qualidade:listarelatorioareaview')
    success_message = "<b>Relatório %(id)s </b>editado com sucesso."
    permission_codename = 'change_relatorioarea'

    def view_context(self, context):
        context['title_complete'] = 'EDITAR RELATÓRIO N°' + \
            str(self.object.id)
        context['return_url'] = reverse_lazy('qualidade:listarelatorioareaview')
        context['tipo_pessoa'] = 'relatorioarea'
        #context['link'] = f"127.0.0.1:8000/cadastro/relatorioarea/pdf/{self.object.id}"
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        return super(EditarRelatorioAreaView, self).get(request, form_class, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        return super(EditarRelatorioAreaView, self).post(request, form_class, *args, **kwargs)

class EditarRelatorioJatoView(EditarDocumentoView):
    form_class = RelatorioJatoForm
    model = RelatorioJato
    template_name = "pessoa_edit.html"
    success_url = reverse_lazy('qualidade:listarelatoriojatoview')
    success_message = "<b>Relatório %(id)s </b>editado com sucesso."
    permission_codename = 'change_relatoriojato'

    def view_context(self, context):
        context['title_complete'] = 'EDITAR RELATÓRIO N°' + \
            str(self.object.id)
        context['return_url'] = reverse_lazy('qualidade:listarelatoriojatoview')
        context['tipo_pessoa'] = 'relatoriojato'
        materiais_sem_relatorio = Material.objects.filter(relatorio__isnull=True)
        materiais_do_relatorio = Material.objects.filter(relatorio=self.object.id)
        context['materiais_sem_relatorio'] = materiais_sem_relatorio
        context['materiais_do_relatorio'] = materiais_do_relatorio
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        return super(EditarRelatorioJatoView, self).get(request, form_class, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        return super(EditarRelatorioJatoView, self).post(request, form_class, *args, **kwargs)

    
class PhotoCreateViewJato(CustomCreateView):
    template_name = 'photo_form.html'
    form_class = PhotoForm
    success_url = reverse_lazy('qualidade:listarelatoriojatoview')
    success_message = "<b>Foto  %(id)s </b> adicionada com sucesso."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['title_complete'] = f'ADICIONAR FOTO AO RELATÓRIO Nº{self.kwargs["pk"]}'
        return context

    def form_valid(self, form):
        form.instance.rip_numero_id = self.kwargs['pk']
        return super().form_valid(form)
    
class PhotoCreateViewArea(CustomCreateView):
    template_name = 'photo_form.html'
    form_class = PhotoForm
    success_url = reverse_lazy('qualidade:listarelatorioareaview')
    success_message = "<b>Foto  %(id)s </b> adicionada com sucesso."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['title_complete'] = f'ADICIONAR FOTO AO RELATÓRIO Nº{self.kwargs["pk"]}'
        return context

    def form_valid(self, form):
        form.instance.rip_numero_id = self.kwargs['pk']
        return super().form_valid(form)


def delete_photoarea(request, pk):
    photo = Photo.objects.get(pk=pk)
    photo.delete()
    return redirect('qualidade:listarelatorioareaview')

def delete_photojato(request, pk):
    photo = Photo.objects.get(pk=pk)
    photo.delete()
    return redirect('qualidade:listarelatoriojatoview')


def render_pdf_view(request, pk):
    relatorio = get_object_or_404(Relatorio, pk=pk)
    template_path = 'rip.html'
    teste = relatorio.relatorio.all()
    links = []
    for item in teste:
        if item.photo:
            link = item.photo.url
            link = link[1:]
            links.append(link)
    context = {'relatorio': relatorio,'links':links}
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

def render_pdf_view_simple(request, pk):
    checklist = get_object_or_404(Relatorio, pk=pk)
    template_path = 'rip_simp.html'
    teste = checklist.relatorio.all()
    etapas = checklist.relatorios.all()
    links = []
    ultimo_item = etapas[0:]
    espessura_total = 0
    ambiente = checklist.ambiente_pintura
    for y in etapas:
        if y.eps:
            espessura_total += float(y.eps)
    for x in ultimo_item:
        cor = x.cor_munsell
        aderencia = x.aderencia
    for item in teste:
        if item.photo:
            link = item.photo.url
            link = link[1:]
            links.append(link)
    context = {'object': checklist, 'links':links, 'cor':cor, 'espessura_total':espessura_total, 'aderencia':aderencia,'ambiente':ambiente}
   
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def atualizar_materiais_selecionados(request):
    if request.method == 'POST':
        vi = request.POST.get('valores_materiais')
        id = request.POST.get('valores_id')
        vi = str(vi)
        present = vi.split(",")
        present.pop()
        for i in present:
            if not i == "null":
                Material.objects.filter(pk=i).update(relatorio=id)
        url='qualidade:editarrelatoriojatoview'
        return HttpResponseRedirect(resolve_url(url,id))
    
