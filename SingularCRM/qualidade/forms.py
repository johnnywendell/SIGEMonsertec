from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms import inlineformset_factory

from .models import EtapaPintura, RelatorioArea, RelatorioJato, Relatorio, Photo

class RelatorioForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RelatorioForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ('cliente','data','rec','tag','nota', 'tipo_serv', 'unidade', 'setor', 'corrosividade', 'fiscal', 'inspetor', 
                  'inicio','termino','tratamento', 'tipo_subs', 'temp_ambiente', 'ura', 'po', 'temp_super', 'intemperismo', 
                  'descontaminacao', 'poeira_tam', 'poeira_quant', 'teor_sais', 'ambiente_pintura', 'rugosidade', 
                  'laudo', 'obs_inst', 'obs_final', 'aprovado')
        widgets = {
            'cliente':forms.TextInput(attrs={'class': 'form-control'}),
            'data':forms.DateInput(attrs={'class': 'form-control datepicker'}),         
            'rec':forms.TextInput(attrs={'class': 'form-control'}), 
            'nota':forms.TextInput(attrs={'class': 'form-control'}), 
            'tag':forms.TextInput(attrs={'class': 'form-control'}), 
            'tipo_serv':forms.Select(attrs={'class': 'form-control'}),
            'unidade':forms.Select(attrs={'class': 'form-control'}), 
            'setor':forms.TextInput(attrs={'class': 'form-control'}),
            'corrosividade':forms.Select(attrs={'class': 'form-control'}), 
            'fiscal':forms.TextInput(attrs={'class': 'form-control'}), 
            'inspetor':forms.TextInput(attrs={'class': 'form-control'}),
            'inicio':forms.DateInput(attrs={'class': 'form-control datepicker'}),  
            'termino':forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'tratamento':forms.TextInput(attrs={'class': 'form-control'}), 
            'tipo_subs':forms.TextInput(attrs={'class': 'form-control'}),
            'temp_ambiente':forms.TextInput(attrs={'class': 'form-control'}),
            'ura' :forms.TextInput(attrs={'class': 'form-control'}),
            'po' :forms.TextInput(attrs={'class': 'form-control'}),
            'temp_super':forms.TextInput(attrs={'class': 'form-control'}), 
            'intemperismo':forms.TextInput(attrs={'class': 'form-control'}), 
            'descontaminacao' :forms.TextInput(attrs={'class': 'form-control'}),
            'poeira_tam':forms.TextInput(attrs={'class': 'form-control'}), 
            'poeira_quant':forms.TextInput(attrs={'class': 'form-control'}),
            'teor_sais':forms.TextInput(attrs={'class': 'form-control'}), 
            'ambiente_pintura':forms.Select(attrs={'class': 'form-control'}), 
            'rugosidade':forms.TextInput(attrs={'class': 'form-control'}), 
            'laudo':forms.CheckboxInput(attrs={'class': 'form-control'}),
            'obs_inst':forms.Textarea(attrs={'class': 'form-control'}),
            'obs_final':forms.Textarea(attrs={'class': 'form-control'}),
            'aprovado':forms.CheckboxInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'cliente':_('Cliente'),
            'data':_('Data'),           
            'rec':_('REC/DOC/REF'), 
            'nota':_('Nota'), 
            'tag':_('Tag'), 
            'tipo_serv':_('Tipo de Serviço'),
            'unidade':_('Unidade/Area'), 
            'setor':_('Setor'),
            'corrosividade':_('Corrosividade'), 
            'fiscal':_('Fiscal'), 
            'inspetor':_('Inspetor'),
            'inicio':_('Data ínicio'),
            'termino':_('Data término'),
            'tratamento':_('Tratamento'), 
            'tipo_subs':_('Tipo de Substrato'),
            'temp_ambiente':_('Temperatura Ambiente'),
            'ura' :_('Úmidade Relativa'),
            'po' :_('Ponto de Orvalho'),
            'temp_super':_('Temperatura do substrato'), 
            'intemperismo':_('Intemperismo'), 
            'descontaminacao' :_('Descontaminacao'),
            'poeira_tam':_('Teste de Poeira(Tamanho)'), 
            'poeira_quant':_('Teste de Poeira(Qtd)'),
            'teor_sais':_('Teor de Sais'), 
            'ambiente_pintura':_('Ambiente Pintura(int/ext)'), 
            'rugosidade':_('Rugosidade'), 
            'laudo':_('Laudo'),
            'obs_inst':_('Instrumentos'),
            'obs_final':_('Observações'),
            'aprovado':_('Aprovação'),
            
        }
        def save(self, commit=True):
            instance = super(RelatorioForm, self).save(commit=False)
            instance.criado_por = self.request.user
            if commit:
                instance.save()
            return instance

class RelatorioAreaForm(RelatorioForm):
    class Meta(RelatorioForm.Meta):
        model = RelatorioArea
        fields = RelatorioForm.Meta.fields + ('m2','calha_utec', 'guia_pc', 'fita_protec', 'trecho_rec', 'elastomero', 'volante_caps')

        widgets = {
            **RelatorioForm.Meta.widgets,
            'm2': forms.TextInput(attrs={'class': 'form-control'}),
            'calha_utec': forms.Select(attrs={'class': 'form-control'}),
            'guia_pc': forms.Select(attrs={'class': 'form-control'}),
            'fita_protec': forms.Select(attrs={'class': 'form-control'}),
            'trecho_rec': forms.Select(attrs={'class': 'form-control'}),
            'elastomero': forms.Select(attrs={'class': 'form-control'}),
            'volante_caps': forms.Select(attrs={'class': 'form-control'}),
        }
        
        labels = {
            **RelatorioForm.Meta.labels,
            'm2': _('M2'),
            'calha_utec': _('Calha UTEC'),
            'guia_pc': _('Guias/Pontos de contato'),
            'fita_protec': _('Fita de Proteção'),
            'trecho_rec': _('Trechos recomendados'),
            'elastomero': _('Elastômero'),
            'volante_caps': _('Volantes/Caps'),
        }

class RelatorioJatoForm(RelatorioForm):
    def __init__(self, *args, **kwargs):
        super(RelatorioJatoForm, self).__init__(*args, **kwargs)
   
    class Meta(RelatorioForm.Meta):
        model = RelatorioJato
        fields = RelatorioForm.Meta.fields  
        widgets = RelatorioForm.Meta.widgets
        labels = RelatorioForm.Meta.labels

class EtapaPinturaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EtapaPinturaForm, self).__init__(*args, **kwargs)

    class Meta:
        model = EtapaPintura 

        fields = ( 'tinta', 'lote_a', 'val_a', 'lote_b', 'val_b', 'lote_c', 'val_c', 'cor_munsell', 
                  'temp_amb', 'ura', 'po', 'temp_substrato', 'diluente', 'met_aplic', 'inicio', 'termino', 
                  'inter_repintura', 'epe', 'eps', 'insp_visual', 'aderencia', 'holiday', 'laudo', 'data_insp', 'pintor')
        widgets = { 
                    'tinta':forms.TextInput(attrs={'class': 'form-control'}),
                    'lote_a':forms.TextInput(attrs={'class': 'form-control'}),
                    'val_a':forms.DateInput(attrs={'class': 'form-control datepicker'}),  
                    'lote_b':forms.TextInput(attrs={'class': 'form-control'}),
                    'val_b':forms.DateInput(attrs={'class': 'form-control datepicker'}),  
                    'lote_c':forms.TextInput(attrs={'class': 'form-control'}),
                    'val_c':forms.DateInput(attrs={'class': 'form-control datepicker'}),  
                    'cor_munsell':forms.TextInput(attrs={'class': 'form-control'}),
                    'temp_amb':forms.TextInput(attrs={'class': 'form-control'}),
                    'ura':forms.TextInput(attrs={'class': 'form-control'}),
                    'po':forms.TextInput(attrs={'class': 'form-control'}),
                    'temp_substrato':forms.TextInput(attrs={'class': 'form-control'}),
                    'diluente':forms.TextInput(attrs={'class': 'form-control'}),
                    'met_aplic':forms.TextInput(attrs={'class': 'form-control'}),
                    'inicio':forms.DateInput(attrs={'class': 'form-control datepicker'}),  
                    'termino':forms.DateInput(attrs={'class': 'form-control datepicker'}),  
                    'inter_repintura':forms.TextInput(attrs={'class': 'form-control'}),
                    'epe':forms.TextInput(attrs={'class': 'form-control'}),
                    'eps':forms.TextInput(attrs={'class': 'form-control'}),
                    'insp_visual':forms.Select(attrs={'class': 'form-control'}),
                    'aderencia':forms.TextInput(attrs={'class': 'form-control'}),
                    'holiday':forms.TextInput(attrs={'class': 'form-control'}),
                    'laudo':forms.Select(attrs={'class': 'form-control'}),
                    'data_insp':forms.DateInput(attrs={'class': 'form-control datepicker'}),  
                    'pintor':forms.TextInput(attrs={'class': 'form-control'}),
            
        }
        labels = {
                    'tinta':_('Tinta'),
                    'lote_a':_('Lote a'),
                    'val_a':_('Validade a'),
                    'lote_b':_('Lote b'),
                    'val_b':_('Validade b'),
                    'lote_c':_('Lote c'),
                    'val_c':_('Validade c'),
                    'cor_munsell':_('Cor'),
                    'temp_amb':_('Temperatura Ambiente'),
                    'ura':_('Úmidade relativa'),
                    'po':_('Ponto de Orvalho'),
                    'temp_substrato':_('Temperatura Substrato'),
                    'diluente':_('Diluente'),
                    'met_aplic':_('Método aplic.'),
                    'inicio':_('Data ínicio'),
                    'termino':_('Data término'),
                    'inter_repintura':_('Intervalo de repintura'),
                    'epe':_('Espessura especificada'),
                    'eps':_('Espessura seca'),
                    'insp_visual':_('INspeção Visual'),
                    'aderencia':_('Aderência'),
                    'holiday':_('Holiday'),
                    'laudo':_('Laudo'),
                    'data_insp':_('Data inspeção'),
                    'pintor':_('Pintor/Executante'),
        }
class PhotoForm(forms.ModelForm): 
    required_css_class = 'required'
    photo = forms.ImageField(required=False)
    class Meta:
        model = Photo
        fields = '__all__'
       
    def __init__(self, *args, **kwargs):
        super(PhotoForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['photo'].widget.attrs['class'] = None

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        # Tamanho máximo permitido em bytes (2MB)
        max_size = 2 * 1024 * 1024

        if photo and photo.size > max_size:
            raise forms.ValidationError('O tamanho máximo da imagem deve ser de 2MB.')

        return photo
    
EtapaFormSet = inlineformset_factory(
    Relatorio, EtapaPintura, form=EtapaPinturaForm, extra=1, can_delete=True)


