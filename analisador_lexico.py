# -*- coding: utf-8 -*-
"""
O objetivo da análise léxica é receber uma sequência de caracteres e
produzir uma sequência de palavras chaves, pontuação e nomes.
Essa sequência de palavras é denominada tokens.
Descartando comentários e espaços em branco.

Tokens
    Em português:
        • substantivo, verbo, adjetivo...
    Em uma linguagem de programação:
        • identificador, numeral, if, while, (, ;, identação, ...)

    Tipos:
        • Identificador = strings de letras ou dígitos, começadas por letra;
        • Numeral = strings de dígitos;
        • Espaço em branco = uma string de brancos, quebras de linha, tabs, ou
        comentários, neste caso é descartado;
        • Palavra reservada = white, if, else;

Exemplo: 
    if (x == y) {
        z = 1;
    }
        
if| |(| |x| |==| |y| |{|\n |z| |=| |1|;|\n| |}|<EOF>

<RC: 4, 'if'> <'SP', '('> <'ID', 'x'> <'OP', '=='> <'ID', 'y'> ...

Obs.: <EOF> é End of file, <RC> é palavra reservada, <SP> é separador,
<ID> é identificar, <OP> é operador
"""

from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
import re
from analisador_sintatico import Sintatico

separadores = [';', '[', ']', ')', '(', ')', '{', '}', ',', '=', '.']
operadores = ['-', '+', '/', '*', '^', '%', '!', '>', '<', "&"]
# operadores_dobrados = ['--', '++', '==', '&&', '||', '<=', '>=', '!=']
token = ""
numerico = ""
estado = 0 # Variável de controle
linha = 0
coluna = 0
id_tabela = 0
acumula = ""
lista_erros = []
token_geral = []
tabela_token = {}

# Verifica se o token geral apresenta um erro. Isso é feito fazendo
# a comparação com os separadores e com os operadores
# Caso não encontre gera '[Token Inválido]'
def verifica_lexico(elemento, token_geral, lista_erros, linha, coluna):
    """Se apresentar erro retorna 1 e se for bem sucessido retorna 0"""
    # token_invalido = 0
    separ_oper = separadores + operadores
    if not re.match("[\w]", elemento):
        if elemento not in separ_oper:
            if not re.search(r"\s", elemento):
                token_geral.append("[Token Inválido]")
                lista_erros.append(
                    [elemento, add_linha_coluna(elemento, linha, coluna)])
            return 0
    return 1

def aux_agrupa(elemento, i, lista, cont, elemento_double, next_elemento):
    """Auxilia a função que agrupa"""
    if elemento in i:
        if (cont + 1) < len(lista):
            if next_elemento in lista[cont + 1]:
                lista.pop(cont + 1)
                lista.insert(cont, [elemento_double])
                lista.pop(cont + 1)
                
# Trata os casos de operadores e elementos especiais
def agrupa(lista):
    """Agrupa os elementos na lista"""
    cont = 0
    # print(lista)
    for i in lista:
        aux_agrupa("+", i, lista, cont, "++", "+")
        aux_agrupa("-", i, lista, cont, "--", "-")
        aux_agrupa("=", i, lista, cont, "==", "=")
        aux_agrupa("&", i, lista, cont, "&&", "&")
        aux_agrupa("|", i, lista, cont, "||", "|")
        aux_agrupa("<", i, lista, cont, "<=", "=")
        aux_agrupa(">", i, lista, cont, ">=", "=")
        aux_agrupa("!", i, lista, cont, "!=", "=")
        cont = cont + 1

def add_linha_coluna(token, linha, coluna):
    """Adiciona linha e coluna"""
    p_inicio = coluna - len(token)
    return "L:" + str(linha) + " C:(" + str(p_inicio) + "," + str(coluna) + ")"

# Os identificadores correspondem a qualquer caractere de palavra
def ver_iden(elemento):
    """Verifica se o elemento é um separador dos números"""
    if(re.match(r"[\w]", elemento)):
        return 0
    else:
        """Se ele não pertence, retorna 1"""
        return 1

# Constantes numéricas correspondem a qualquer dígito decimal
def ver_num(elemento):
    """Verifica se o elemento pertence ao grupo das constantes numéricas"""
    if(re.match(r"[\d.]", elemento)):
        return 0
    else:
        """Se ele não pertence retorna 1"""
        return" 1"
        
"""
Tokens reservados são as palavras definidas como padrão para o algoritmo
Neste algoritmo foi definido três tipos de variáveis (int, float e char),
duas estruturas de repetição (for e while), entrada e saída de dados (printf e read),
duas declarações para alterar o fluxo (continue e break)
e declarações de decisão (if e else)
"""

def verifica_reservada(token):
    """Verifica se o token é reservado e retorna o indice para o mesmo"""
    reservada_lista = ['int', 'float', 'char', 'if', 'else', 'printf',
                      'for', 'while', 'return', 'continue', 'break', 'read']
    cont = 0
    for i in reservada_lista:
        cont = cont + 1
        if (token == i):
            return cont

def exibe_imprime(nome, lista):
    """Escreve no Arquivo de Saída"""
    arq = open(nome, "w")
    if(len(lista) == 0):
        arq.write("Lista vazia!\n")
    for i in lista:
        print(i)
        arq.write(str(i) + "\n")
    arq.close()

def imprime_tabela(tabela_token):
    """Imprime a tabela de tokens"""
    arq_tabela = open("tabela_simbolos_simp", "w")
    arq_tabela.write("Tabela de Simbolos\n")
    for i in sorted(tabela_token):
        arq_tabela.write("Chave:" + str(i) + " " + str(tabela_token[i]) + "\n")
    arq_tabela.close()

def open_file():
    """Abre o arquivo de entrada"""
    try:
        Tk().withdraw()
        file_path = askopenfilename()
        arquivo = open(file_path, "r")
    except Exception as e:
        print("Exception: ", e)
    return arquivo

arquivo = open_file()
"""
Aqui é feita a leitura e conversão do arquivo. Foi feita através de uma máquina de estados
chamada de estado, onde cada indice indica uma ação determinada pelo léxico que no caso é
feita atráves de um Regex
estado 0 = Estado Inicial
estado 1 = Validação de Identificador
estado 2 = Indentificação de Constante Numérica
estado 3 = Identificação de Literal
estado 4 = Incrementa Comentário
"""
for i in arquivo:
    linha = linha + 1
    coluna = 0
    for j in i:
        id_tabela = (id_tabela + 1)
        coluna = coluna + 1
        """Estado inicial"""
        if estado == 0:
            if j == "/" and i[coluna] == "*" and estado == 0 and estado != 4:
                """Pesquisa por Comentario"""
                estado = 4
                token_geral.append(["*/"])
            if re.search(r"^(#)|[/]{2}", i) and estado == 0 and estado != 4:
                """Ignora o stdio e linha comentada"""
                break
            if re.match(r"([A-Za-z_])", j) and estado == 0 and estado != 4:
                """Pesquisa por identificadores validos de Aa a zZ"""
                estado = 1  # Identificador
            if re.match(r"[0-9]", j) and estado == 0 and estado != 4:
                """Pesquisa por Constante Numérica de 0 a 9"""
                estado = 2  # Constante Numérica
            if re.match(r"[\"]", j) and estado == 0 and estado != 4:
                """Pesquisa por Literal"""
                estado = 3 # Literal
            if ver_num(j) and ver_iden(j) and estado == 0 and estado != 4:
                """Se não for um identificador valido então é um separador"""
                if verifica_lexico(j, token_geral, lista_erros, linha, coluna):
                    token_geral.append([j])
        """Valida Identificador"""
        if estado == 1:
            if re.match(r"([\w])", j):
                token = token + j
            if ver_iden(j):
                """Lista com separadores"""
                estado = 0
                if verifica_reservada(token):
                    tabela_token[id_tabela] = ["RES: " + str(
                        verifica_reservada(token)), token, add_linha_coluna(token, linha, coluna)]
                    token_geral.append(
                        ["RES: " + str(verifica_reservada(token)), token, id_tabela])
                    if j != " ":
                        if verifica_lexico(j, token_geral, lista_erros, linha, coluna):
                            token_geral.append([j])
                    token = ""
                else:
                    tabela_token[id_tabela] = ["ID", token,
                                               add_linha_coluna(token, linha, coluna)]
                    token_geral.append(
                        ["ID", token, id_tabela])
                    if ver_iden(j):
                        """Vai inserir o j como separador """
                        if j is not re.match(r"\s", j):
                            if verifica_lexico(j, token_geral, lista_erros, linha, coluna):
                                """Se não encontrar um erro insere"""
                                token_geral.append([j])
                        estado = 0
                    token = ""
        """Indentificação de Constante Numérica"""
        if estado == 2:
            if re.match(r"[\w.]", j):
                numerico = numerico + j
            if ver_num(j):
                if(re.match(r"(^[0-9]*$|[0-9]+.[0-9]+)", numerico)):
                    valor = re.match(r"(^[0-9]*$|[0-9]+.[0-9]+)", numerico)
                    if valor is not None:
                        tabela_token[id_tabela] = [
                            "NUM", valor.group(), add_linha_coluna(valor.group(), linha, coluna)]
                        token_geral.append(
                            ["NUM", valor.group(), id_tabela])
                        if j != " ":
                            if verifica_lexico(j, token_geral, lista_erros, linha, coluna):
                                token_geral.append([j])
                        estado = 0
                        numerico = ""
                else:
                    if j in separadores or re.match(r"\s|\n", j) or j in operadores:
                        """Identifica o token/separador inválido"""
                        token_geral.append("[Token Inválido]")
                        lista_erros.append(
                            [numerico, add_linha_coluna(numerico, linha, coluna)])
                        numerico = ""
                        estado = 0
            else:
                if ver_num(j):
                    "Armazena token de separadores"
                    if j != " ":
                        if verifica_lexico(j, token_geral, lista_erros, linha, coluna):
                            token_geral.append([j])
                    estado = 0
        """Identifica Literal"""
        if estado == 3:
            if re.match(r"[%a-zA-z0-9\"\s]", j):
                token = token + j
                if re.match(r"[\"]", j):
                    lit = re.match(r"[\"]+[%\w\s]+[\"]*", token)
                    if lit is not None:
                        tabela_token[id_tabela] = ["LIT", lit.group(
                        ), add_linha_coluna(lit.group(), linha, coluna)]
                        token_geral.append(
                            ["LIT", lit.group(), id_tabela])
                        token = ""
                        estado = 0
        """Incrementa comentarios"""
        if estado == 4:
            acumula = acumula + j
            if re.search(r"(\*\/)", acumula):
                token_geral.append("[*/]")
                estado = 0

if __name__ == '__main__':
    sin = Sintatico()
    agrupa(token_geral)
    # print(token_geral)
    exibe_imprime("token_saida", token_geral)
    # print(token_geral)
    sin.conector(token_geral, tabela_token)
    # print("Erros ", exibe_imprime("lista_erros", lista_erros))
    # lista_erros = []
    # print("Tabela", tabela_token)
    imprime_tabela(tabela_token)
    # print("Comentário:", acumula)