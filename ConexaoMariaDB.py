# Module Imports
import MySQLdb
import sys

try:
    conn = MySQLdb.connect(host="jobs.visie.com.br",
                           user="allanramos",
                           passwd="c6ed7d5ae0c0a5ca6be17706afcffd0f",
                           db="allanramos",
                           port=3306)
except MySQLdb.Error as e:
    print(f"Erro ao conectar à plataforma MariaDB: {e}")
    sys.exit(1)

cursor = conn.cursor()


def criar_tabela():
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS informacao (id_usuario INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY, nome VARCHAR(100) NOT NULL, sobrenome VARCHAR(100) NOT NULL, rg VARCHAR(12) NOT NULL, cpf VARCHAR(14) NOT NULL, data_aniversario DATE NOT NULL, logradouro VARCHAR(255) NOT NULL, complemento VARCHAR(255) NOT NULL, bairro VARCHAR(255) NOT NULL, localidade VARCHAR(255) NOT NULL, uf VARCHAR(2) NOT NULL, cep VARCHAR(9) NOT NULL, dinheiro_real numeric(20, 2) NOT NULL, dinheiro_dolar  numeric(20, 2) NOT NULL, profissao VARCHAR(255) NOT NULL, mercado VARCHAR(255) NOT NULL, salario_real  numeric(20, 2) NOT NULL, salario_dolar  numeric(20, 2) NOT NULL)")


def insert_tabela(informacao):
    try:
        sql = "INSERT INTO informacao (nome, sobrenome, rg, cpf, data_aniversario, logradouro, complemento, bairro, localidade, uf, cep, dinheiro_real, dinheiro_dolar, profissao, mercado, salario_real, salario_dolar) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.executemany(sql, informacao)
    except MySQLdb.Error as e:
        print(f"Error: {e}")

    conn.commit()

    conn.close()


criar_tabela()

