from datetime import datetime
import csv
import io
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from cadastro.models import geral as b


########### import csv ##############

def save_data(data):
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
        obj = b.ItemBm(
                contrato = b.Contrato.objects.get(pk=contrato),
                item_ref = item_ref,
                disciplina = disciplina,
                descricao = descricao,
                und = und,
                preco_item = preco_item,
        )
        aux.append(obj)
    b.ItemBm.objects.bulk_create(aux)

def import_csv_itembm(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        # Lendo arquivo InMemoryUploadedFile
        file = myfile.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(file))
        # Gerando uma list comprehension
        data = [line for line in reader]
        save_data(data)
        return HttpResponseRedirect(reverse('cadastro:listaitensmedview'))
    template_name = 'model_import.html'
    title_import = 'ITENS DE CONTRATO (csv)'
    context = {'title_import': title_import}
    return render(request, template_name,context=context)