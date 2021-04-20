import json

import Conexao_mdb
# from models import Informacao
from utils import get_dict_taxas_atuais, apenas_digitos, buscar_endereco_por_cep, moeda, ingles_para_portugues


class Importador():
    def __init__(self):
        print('Iniciando importação...')
        import pandas as pd
        # Variavel count apenas pra exibir no terminal a interação com a importação
        count = 0

        df_dados_pessoais = pd.read_excel(
            'https://jobs.visie.com.br/teste-pratico/integracao-de-dados/dados-pessoais.xlsx')
        df_dados_complementares = json.loads(
            pd.read_csv('https://jobs.visie.com.br/teste-pratico/integracao-de-dados/dados-complementares.csv').to_json(
                orient="records"))
        dict_moeda_taxa_atuais = get_dict_taxas_atuais()

        taxa_dolar_em_reais = dict_moeda_taxa_atuais['BRL'] / dict_moeda_taxa_atuais['USD']

        informacao = []
        for posicao, valor in enumerate(json.loads(df_dados_pessoais.to_json(orient="records"))):
            count = count + 1

            nome = valor['Nome completo'].split(" ", 1)[0]
            sobrenome = valor['Nome completo'].split(" ", 1)[1]
            rg = valor['RG']
            cpf = valor['CPF']
            data_aniversario = pd.to_datetime(valor['Data de aniversário'], unit='ms').to_pydatetime()

            cep = valor['CEP']
            dict_endereco = buscar_endereco_por_cep(apenas_digitos(cep))
            logradouro = dict_endereco.get('logradouro', 'CEP inexistente')
            complemento = dict_endereco.get('complemento', '')
            bairro = dict_endereco.get('bairro', '')
            localidade = dict_endereco.get('localidade', '')
            uf = dict_endereco.get('uf', '')

            dinheiro_real = moeda(valor['Dinheiro'], 'real')
            dinheiro_dolar = moeda(valor['Dinheiro'] / taxa_dolar_em_reais, 'dolar')

            profissao = ingles_para_portugues(str(df_dados_complementares[posicao]['department']))
            mercado = ingles_para_portugues(str(df_dados_complementares[posicao]['market']))

            salario_dolar = df_dados_complementares[posicao]['wage']
            if salario_dolar is None:
                salario_dolar = moeda(0.0, 'dolar')
                salario_real = moeda(0.0, 'real')

            else:
                salario_real = moeda(float(salario_dolar.replace('$', '')) * taxa_dolar_em_reais, 'real')


            tupla = (nome, sobrenome, rg, cpf, data_aniversario.date(), logradouro, complemento, bairro,
                 localidade, uf, cep, dinheiro_real, dinheiro_dolar, profissao, mercado, salario_real, salario_dolar)

            informacao.append(tupla)
            print(count)
        Conexao_mdb.insert_tabela(informacao)
        print('Importação concluída com sucesso!')

            ###Falta colocar ou tirar as maskaras



