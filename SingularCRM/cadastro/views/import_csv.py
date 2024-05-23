from datetime import datetime
import csv
import io
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from cadastro.models import geral
from efetivo.models import Colaborador


########### import csv ##############

def save_data_itembm(data):
    '''
    Salva os dados no banco.
    '''
    aux = []
    for item in data:
        contrato = 1
        item_ref = item.get('item_ref')
        disciplina = item.get('disciplina')
        descricao = item.get('descricao')
        und = item.get('und')
        preco_item = item.get('preco_item')
        obj = geral.ItemBm(
                contrato = b.Contrato.objects.get(pk=contrato),
                item_ref = item_ref,
                disciplina = disciplina,
                descricao = descricao,
                und = und,
                preco_item = preco_item,
        )
        aux.append(obj)
    geral.ItemBm.objects.bulk_create(aux)

def import_csv_itembm(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        # Lendo arquivo InMemoryUploadedFile
        file = myfile.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(file))
        # Gerando uma list comprehension
        data = [line for line in reader]
        save_data_itembm(data)
        return HttpResponseRedirect(reverse('cadastro:listaitensmedview'))
    template_name = 'model_import.html'
    title_import = 'ITENS DE CONTRATO (csv)'
    context = {'title_import': title_import}
    return render(request, template_name,context=context)


#####
def save_data_colaboradores(data):
    '''
    Salva os dados no banco.
    '''
    aux = []
    for item in data:
        nome = item.get('nome')
        matricula = item.get('matricula')
        funcao = item.get('funcao')
        ativo = True
        obj = Colaborador(
                nome = nome,
                matricula = matricula,
                funcao = funcao,
                ativo = ativo,
        )
        aux.append(obj)
    Colaborador.objects.bulk_create(aux)

def import_csv_colaboradores(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        # Lendo arquivo InMemoryUploadedFile
        file = myfile.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(file))
        # Gerando uma list comprehension
        data = [line for line in reader]
        save_data_colaboradores(data)
        return HttpResponseRedirect(reverse('efetivo:listacolaboradoreview'))
    template_name = 'model_import.html'
    title_import = 'COLABORADORES (csv)'
    context = {'title_import': title_import}
    return render(request, template_name,context=context)
