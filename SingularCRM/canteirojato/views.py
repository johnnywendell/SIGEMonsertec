
from core.custom_views import CustomView, CustomCreateView, CustomListView, CustomUpdateView
from .forms import RomaneioForm, MaterialFormSet
from .models import Romaneio, Material
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def json_fatores(request):
    data = {
            'perfil_I':{'3':0.41,'4':0.50,'5':0.59,'6':0.68,'8':0.84,'10':1.03,'12':1.18,'14':1.35,'18':1.53,'20':1.76,'22':1.94,'24':2.13,'26':2.32},
            'perfil_H':{'4':0.61,'5':0.77,'6':0.92,'7':1.08,'8':1.23,'9':1.39,'10':1.54,'11':1.70,'12':1.85,'13':2.01,'14':2.16,'15':2.32,'16':2.47,'17':2.63,'18':2.78,'19':2.94,'20':3.09},
            'perfil_U':{'3':0.32,'4':0.38,'6':0.56,'8':0.68,'10':0.84,'12':0.96,'14':1.15,'16':1.29,'18':1.45,'20':1.60,'22':1.76,'24':1.91,'26':2.07},
            'perfil_L':{'1':0.10,'2':0.20,'2,5':0.26,'3':0.31,'4':0.41,'5':0.51,'6':0.61,'8':0.82,'10':1.03,'12':1.24},
            'barra_chata':{'0,5':0.03,'1':0.05,'2':0.10,'2,5':0.13,'3':0.15,'4':0.20,'5':0.25,'6':0.30,'8':0.41,'10':0.51,'12':0.61},
            'tubulacao':{'0,5':0.08,'0,75':0.1,'1':0.13,'1,5':0.16,'2':0.21,'2,5':0.25,'3':0.31,'4':0.39,'6':0.57,'8':0.73,'10':0.9,'12':1.07,'14':1.18,'16':1.36,'18':1.52,'20':1.68,'22':1.84,'24':2,'26':2.18,
            '28':2.35,'30':2.51,'32':2.68,'34':2.85,'36':3.01,'38':3.18,'40':3.35,'44':4.00,'50':4.21,'52':4.42,'54':4.63,'56':4.84,'58':5.05,'60':5.26},
            'acess_T':{'0,5':0.01,'0,75':0.01,'1':0.01,'1,5':0.01,'2':0.02,'2,5':0.02,'3':0.03,'4':0.05,'6':0.11,'8':0.18,'10':0.26,'12':0.37,'14':0.45,'16':0.62,'18':0.78,'20':0.96,'22':1.12,'24':1.38,
            '26':1.62,'28':1.89,'30':2.15,'32':2.37,'34':2.61,'36':2.86,'38':3.10,'40':3.34,'44':3.58,'50':3.83,'52':4.07,'54':4.31,'56':4.56,'58':4.80,'60':5.04},
            'acess_FLG':{'0,5':0.01,'0,75':0.01,'1':0.01,'1,5':0.01,'2':0.02,'2,5':0.02,'3':0.03,'4':0.05,'6':0.11,'8':0.18,'10':0.26,'12':0.37,'14':0.45,'16':0.62,'18':0.78,'20':0.96,'22':1.12,'24':1.38,
            '26':1.62,'28':1.89,'30':2.15,'32':2.37,'34':2.61,'36':2.86,'38':3.10,'40':3.34,'44':3.58,'50':3.83,'52':4.07,'54':4.31,'56':4.56,'58':4.80,'60':5.04},
            'acess_RED':{'0,5':0.01,'0,75':0.01,'1':0.01,'1,5':0.01,'2':0.02,'2,5':0.02,'3':0.03,'4':0.05,'6':0.11,'8':0.18,'10':0.26,'12':0.37,'14':0.45,'16':0.62,'18':0.78,'20':0.96,'22':1.12,'24':1.38,
            '26':1.62,'28':1.89,'30':2.15,'32':2.37,'34':2.61,'36':2.86,'38':3.10,'40':3.34,'44':3.58,'50':3.83,'52':4.07,'54':4.31,'56':4.56,'58':4.80,'60':5.04},
            'acess_CV90':{'0,5':0.01,'0,75':0.01,'1':0.01,'1,5':0.02,'2':0.03,'2,5':0.04,'3':0.06,'4':0.1,'6':0.21,'8':0.36,'10':0.52,'12':0.74,'14':0.94,'16':1.23,'18':1.55,'20':1.92,'22':2.34,'24':2.75,
            '26':3.23,'28':3.77,'30':4.3,'32':4.76,'34':5.25,'36':5.75,'38':6.24,'40':6.74,'44':7.23,'50':7.72,'52':8.22,'54':8.71,'56':9.21,'58':9.70,'60':10.19},
            'acess_CV45':{'0,5':0.01,'0,75':0.01,'1':0.01,'1,5':0.01,'2':0.02,'2,5':0.02,'3':0.03,'4':0.05,'6':0.11,'8':0.18,'10':0.26,'12':0.37,'14':0.45,'16':0.62,'18':0.78,'20':0.96,'22':1.12,'24':1.38,
            '26':1.62,'28':1.89,'30':2.15,'32':2.37,'34':2.61,'36':2.86,'38':3.10,'40':3.34,'44':3.58,'50':3.83,'52':4.07,'54':4.31,'56':4.56,'58':4.80,'60':5.04},
            'acess_VV':{'0,5':0.06,'0,75':0.1,'1':0.14,'1,5':0.28,'2':0.34,'2,5':0.38,'3':0.45,'4':0.59,'6':0.88,'8':1.17,'10':1.54,'12':1.94,'14':2.38,'16':2.82,'18':3.25,'20':3.69,'22':4.14,'24':4.57,'26':5,
            '28':5.55,'30':5.89,'32':6.47,'34':7.22,'36':7.86,'38':8.22,'40':8.85,'44':9.64,'50':10.38,'52':11.12,'54':11.86,'56':12.60,'58':13.34,'60':14.08},
            'acess_VVC':{'0,5':0.09,'0,75':0.15,'1':0.21,'1,5':0.33,'2':0.45,'2,5':0.57,'3':0.68,'4':0.77,'6':1.14,'8':1.52,'10':1.95,'12':2.33,'14':2.84,'16':3.38,'18':3.9,'20':4.43,'22':4.89,'24':5.48,
            '26':6.01,'28':6.52,'30':7.06,'32':7.69,'34':8.22,'36':8.96,'38':9.77,'40':10.65,'44':11.61,'50':12.72,'52':13.83,'54':14.94,'56':16.05,'58':17.16,'60':18.27},
            'acess_CAP':{'0,5':0.01,'0,75':0.01,'1':0.01,'1,5':0.01,'2':0.02,'2,5':0.02,'3':0.03,'4':0.05,'6':0.11,'8':0.18,'10':0.26,'12':0.37,'14':0.45,'16':0.62,'18':0.78,'20':0.96,'22':1.12,'24':1.38,
            '26':1.62,'28':1.89,'30':2.15,'32':2.37,'34':2.61,'36':2.86,'38':3.10,'40':3.34,'44':3.58,'50':3.83,'52':4.07,'54':4.31,'56':4.56,'58':4.80,'60':5.04}
            }
    return JsonResponse({'data':data})

class AdicionarDocumentoView(CustomCreateView):

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.pk)

    def get_context_data(self, **kwargs):
        context = super(AdicionarDocumentoView, self).get_context_data(**kwargs)
        return self.view_context(context)

    def get(self, request, form_class, *args, **kwargs):
        self.object = None

        form = self.get_form(form_class)
        material_form = MaterialFormSet(prefix='material_form')

        return self.render_to_response(self.get_context_data(form=form,
                                                             material_form=material_form,))
                                                             
    def post(self, request, form_class, *args, **kwargs):
        self.object = None
        # Tirar . dos campos decimais
        req_post = request.POST.copy()

        request.POST = req_post

        form = self.get_form(form_class)
        material_form = MaterialFormSet(request.POST, prefix='material_form')

        if (form.is_valid() and material_form.is_valid()):
            self.object = form.save(commit=False)
            self.object.criado_por = self.request.user
            self.object.save()
            material_form.instance = self.object
            material_form.save()

            return self.form_valid(form)

        return self.form_invalid(form=form,
                                 material_form=material_form,
                                 )

class AdicionarRomaneioView(AdicionarDocumentoView):
    form_class = RomaneioForm
    template_name = "pessoa_add.html"
    success_url = reverse_lazy('canteirojato:listaromaneioview')
    success_message = "<b>Romaneio %(id)s </b>adicionado com sucesso."
    permission_codename = 'add_romaneio'

    def view_context(self, context):
        context['title_complete'] = 'ADICIONAR ROMANEIO'
        context['return_url'] = reverse_lazy('canteirojato:listaromaneioview')
        context['tipo_pessoa'] = 'romaneio'
        return context

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(AdicionarRomaneioView, self).get(request, form_class, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(AdicionarRomaneioView, self).post(request, form_class, *args, **kwargs)
    
class DocumentoListView(CustomListView):
    def get_context_data(self, **kwargs):
        context = super(DocumentoListView, self).get_context_data(**kwargs)
        return self.view_context(context)

class RomaneioListView(DocumentoListView):
    template_name = 'pessoa_list.html'
    model = Romaneio
    context_object_name = 'all_romaneios'
    success_url = reverse_lazy('canteirojato:listaromaneioview')
    permission_codename = 'view_romaneio'

    def view_context(self, context):
        context['title_complete'] = 'ROMANEIOS'
        context['add_url'] = reverse_lazy('canteirojato:addromaneioview')
        context['tipo_pessoa'] = 'romaneio'
        return context
    
class EditarDocumentoView(CustomUpdateView):

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.pk)

    def get_context_data(self, **kwargs):
        context = super(EditarDocumentoView, self).get_context_data(**kwargs)
        return self.view_context(context)

    def get(self, request, form_class, *args, **kwargs):

        form = self.get_form(form_class)

        material_form = MaterialFormSet(
            instance=self.object, prefix='material_form')

        if Material.objects.filter(n_romaneio=self.object.pk).count():
            material_form.extra = 0

        return self.render_to_response(self.get_context_data(form=form, material_form=material_form))

    def post(self, request, form_class, *args, **kwargs):
        # Tirar . dos campos decimais
        req_post = request.POST.copy()

        request.POST = req_post

        form = self.get_form(form_class)
        material_form = MaterialFormSet(
            request.POST, prefix='material_form', instance=self.object)

        if (form.is_valid() and material_form.is_valid()):
            self.object = form.save(commit=False)
            self.object.criado_por = self.request.user
            self.object.save()

            material_form.instance = self.object
            material_form.save()

            return self.form_valid(form)

        return self.form_invalid(form=form,
                                 material_form=material_form,)
    
class EditarRomaneioView(EditarDocumentoView):
    form_class = RomaneioForm
    model = Romaneio
    template_name = "pessoa_edit.html"
    success_url = reverse_lazy('canteirojato:listaromaneioview')
    success_message = "<b>Romaneio %(id)s </b>editado com sucesso."
    permission_codename = 'change_romaneio'

    def view_context(self, context):
        context['title_complete'] = 'EDITAR ROMANEIO N°' + \
            str(self.object.id)
        context['return_url'] = reverse_lazy('canteirojato:listaromaneioview')
        context['tipo_pessoa'] = 'romaneio'
        context['link'] = f"127.0.0.1:8000/cadastro/romaneio/pdf/{self.object.id}"
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        return super(EditarRomaneioView, self).get(request, form_class, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        return super(EditarRomaneioView, self).post(request, form_class, *args, **kwargs)



def render_pdf_view_tag(request, pk):
    template_path = "cabine_jato/qrcode.html"
    obj = Romaneio.objects.get(pk=pk)
    link = f"127.0.0.1:8000/cadastro/romaneio/pdf/{obj.pk}"
    context = {'object': obj, 'link':link}
   
    response = HttpResponse(content_type='application/pdf')

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
       html, dest=response)

    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def render_pdf_view(request, pk):
    template_path = "cabine_jato/romaneio.html"
    obj = Romaneio.objects.get(pk=pk)
    materiais = obj.romaneios.all()
    metro_quadrado = 0
    link = f"127.0.0.1:8000/cadastro/romaneio/pdf/{obj.pk}"
    for material in materiais:
        metro_quadrado += material.m2
    context = {'object': obj, 'metro':metro_quadrado, 'link':link}
   
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