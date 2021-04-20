import json

from conexao_banco import ConexaoMariaDB
# from models import Informacao
from importador.utils import get_dict_taxas_atuais, apenas_digitos, buscar_endereco_por_cep, ingles_para_portugues


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
            rg = apenas_digitos(valor['RG'])
            cpf =  apenas_digitos(valor['CPF'])
            data_aniversario = pd.to_datetime(valor['Data de aniversário'], unit='ms').to_pydatetime()

            cep = valor['CEP']
            dict_endereco = buscar_endereco_por_cep(apenas_digitos(cep))
            logradouro = dict_endereco.get('logradouro', 'CEP inexistente')
            complemento = dict_endereco.get('complemento', '')
            bairro = dict_endereco.get('bairro', '')
            localidade = dict_endereco.get('localidade', '')
            uf = dict_endereco.get('uf', '')

            dinheiro_real = valor['Dinheiro']
            dinheiro_dolar = valor['Dinheiro'] / taxa_dolar_em_reais

            profissao = ingles_para_portugues(str(df_dados_complementares[posicao]['department']))
            mercado = ingles_para_portugues(str(df_dados_complementares[posicao]['market']))

            salario_dolar = df_dados_complementares[posicao]['wage']


            if salario_dolar is None:
                salario_dolar =0.0
                salario_real = 0.0

            else:
                salario_dolar = float(df_dados_complementares[posicao]['wage'].replace('$', ''))
                salario_real = salario_dolar * taxa_dolar_em_reais

            tupla = (nome, sobrenome, rg, cpf, data_aniversario.date(), logradouro, complemento, bairro,
                 localidade, uf, cep, dinheiro_real, dinheiro_dolar, profissao, mercado, salario_real, salario_dolar)

            informacao.append(tupla)
            print(count)

        ConexaoMariaDB.insert_tabela(informacao)
        print('Importação concluída com sucesso!')

            ###Falta colocar ou tirar as maskaras



