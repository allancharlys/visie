import json


def mascaraCPF(cpf):
    return '{}.{}.{}-{}'.format(cpf[:3], cpf[3:6], cpf[6:9], cpf[9:])


def mascara_CEP(cep):
    return '{}-{}'.format(cep[:5], cep[5:])

def apenas_digitos(valor):
    import re
    return re.sub('[^0-9]', '', valor)


def converter_string_em_date(string_data):
    from datetime import datetime
    return datetime.strptime(string_data, '%Y-%m-%d')

def buscar_endereco_por_cep(cep):
    import json, urllib.request
    dados = urllib.request.urlopen("https://viacep.com.br/ws/"+cep+"/json/").read()
    return json.loads(dados)


def get_dict_taxas_atuais():
    import xmltodict
    import pandas as pd
    import urllib.request

    dados = urllib.request.urlopen("https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml").read()
    xmlDict = xmltodict.parse(dados)

    df = pd.DataFrame.from_dict(xmlDict)
    res = df.iloc[2]['gesmes:Envelope']['Cube']

    dict_moeda_taxa = {}
    for l in res['Cube']:
        dict_moeda_taxa[f'{l["@currency"]}'] = float(l['@rate'])

    return dict_moeda_taxa



dicionario = {
  'Research and Development': 'Pesquisa e desenvolvimento',
  'Engineering': 'Engenharia',
  'Services': 'Serviços',
  'Support': 'Apoiar',
  'Sales': 'Vendas',
  'Legal': 'Jurídico',
  'Human Resources': 'Recursos Humanos',
  'Marketing': 'Marketing',
  'Product Management': 'Gestão de produtos',
  'Accounting': 'Contabilidade',
  'Business Development': 'Desenvolvimento de negócios',
  'Training': 'Treinamento',
  'Grocery': 'Mercado',
  'Shoes': 'Sapato',
  'Clothing': 'Confecções',
  'Sports': 'Esportes',
  'Tools': 'Ferramentas',
  'Garden': 'Jardim',
  'Beauty': 'Beleza',
  'Electronics': 'Eletrônicos',
  'Movies': 'Filmes',
  'Industrial': 'Industrial',
  'Health': 'Saúde',
  'Music': 'Música',
  'Kids': 'Crianças',
  'Jewelery': 'Jóias',
  'Baby': 'Bebê',
  'Outdoors': 'Ao ar livre',
  'Books': 'Livros',
  'Games': 'Jogos',
  'Toys': 'Brinquedos',
  'Home': 'Casa',
  'Automotive': 'Automotivo'
}

def ingles_para_portugues(texto):
    traduzido = []
    if dicionario.get(texto):
      traducao = dicionario.get(texto)
      traduzido.append(traducao if traducao else texto)
    else:
      texto = texto.split()
      for palavra in texto:
          traducao = dicionario.get(palavra)
          traduzido.append(traducao if traducao else palavra)

    return ' '.join(traduzido)



import locale
def moeda(valor, tipo):
    valor = float(valor)
    if tipo == 'real':
        tipo = 'pt_BR.UTF-8'
        grouping=True
    else:
        tipo = 'en_US.UTF-8'
        grouping=False

    locale.setlocale(locale.LC_ALL, tipo)
    valor = locale.currency(valor, grouping=grouping, symbol=True)
    return valor

