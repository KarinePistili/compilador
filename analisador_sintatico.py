# coding: utf-8
"""
O objetivo da análise sintática é construir uma derivação mais à esquerda para o programa, partindo do símbolo inicial
de modo que cada passo da derivação, o prefixo de terminais da forma sentencial tem que casar com um prefixo da entrada
caso exista mais de uma regra para o não-terminal que vai gerar o próximo passo da derivação, o analisador usa o primeiro
token após esse prefixo para escolher qual regra usar.

Esse processo continua até todo o programa ser derivado ou acontecer um
erro (o prefixo de terminais da forma sentencial não casa com um prefixo do programa)

No caso abaixo temos uma gramática LL(1) ao qual toda predição pode ser feita examinando um único
token à frente.
"""

class Sintatico(object):
    """Ínicio do programa: define as variáveis"""

    def __init__(self):
        self.tokens = []
        self.lista = []
        self.tabela = []
        self.tabela_declaracao = {}
        self.elemento = ["NUM", "ID", "LIT",
                         "int", "float", "char", "while", "if"]
        self.tipo = ["int", "float", "char"]
        self.pos_global = -1
        self.indica_erro = 0
        self.warning = 0
        self.cont = 0
        self.flag = 0

    def E(self, simb, lista, pos):
        """Verifica se pertence a expressão aritmética"""
        if(simb in "NUM" or simb in "ID" or simb in "LIT" or simb == "("):
            self.T(simb, lista, pos)
            self.Elinha(simb, lista, pos)
            self.logicos(simb, lista, pos)
        else:
            self.erro(simb, pos)
            self.indica_erro = 1
            return pos
        return pos

    def logicos(self, simb, lista, pos):
        """Verifica se pertence a expressão lógica"""
        if(simb == ">" or simb == "<"):
            return self.T(simb, lista, pos)
        else:
            return pos

    def T(self, simb, lista, pos):
        if(simb in "NUM" or simb in "ID" or simb in "LIT" or simb == "("):
            self.F(simb, lista, pos)
            self.logicos(simb, lista, pos)
            self.Tlinha(simb, lista, pos)
        else:
            self.erro(simb, pos)
            self.indica_erro = 1
            return pos
        return pos

    def F(self, simb, lista, pos):
        if(simb == "("):
            simb, pos = self.get_next_token(lista, pos)
            self.E(simb, lista, pos)
            if(simb != ")"):
                exit()
        elif(simb in "NUM" or simb in "ID" or simb in "LIT"):
            simb, pos = self.get_next_token(lista, pos)
            return self.Elinha(simb, lista, pos)
        else:
            self.erro(simb, pos)
            self.indica_erro = 1
            return pos
        return pos

    def get_next_token(self, lista, pos):
        """Trás o próximo token e retorna o elemento a sua posição"""
        maximo = len(self.tokens) - 1
        try:
            pos += 1
            return lista[pos], pos
        except Exception as e:
            return lista[maximo], maximo

    def Elinha(self, simb, lista, pos):
        """Válida adição e subtração"""
        if(simb == "+"):
            simb, pos = self.get_next_token(lista, pos)
            retorno_geracao, tipo_retorno = self.gera_codigo("+", pos, None)
            self.T(simb, lista, pos), retorno_geracao, tipo_retorno
            # Elinha(simb, lista, pos)
        elif (simb == ")" or simb == ";"):
            print("Expressão válida")
            return pos
        elif(simb == "-"):
            simb, pos = self.get_next_token(lista, pos)
            retorno_geracao, tipo_retorno = self.gera_codigo("-", pos, None)
            self.T(simb, lista, pos), retorno_geracao, tipo_retorno
        else:
            self.Tlinha(simb, lista, pos)

        return pos

    def Tlinha(self, simb, lista, pos):
        """Válida multiplicação"""
        if(simb == "*"):
            simb, pos = self.get_next_token(lista, pos)
            retorno_geracao, tipo_retorno = self.gera_codigo("*", pos, None)
            self.F(simb, lista, pos), retorno_geracao, tipo_retorno
            self.Tlinha(simb, lista, pos)
        elif(simb == "/"):
            simb, pos = self.get_next_token(lista, pos)
            retorno_geracao, tipo_retorno = self.gera_codigo("/", pos, None)
            return self.F(simb, lista, pos), retorno_geracao, tipo_retorno
        elif (simb == ")" or simb == ";"):
            print("Expressão válida")
        else:
            if(not(simb in "NUM" or simb in "ID" or simb in "LIT")):
                self.erro(simb, pos)
                self.indica_erro = 1
        return pos

    def warning_inicializado(self, pos):
        """Warning Variavel sem inicializar"""
        print("Atenção: Varíavel sem inicializar Linha"), self.consulta_tabela(pos)[0]
        self.warning = 1

    def valido(self, pos):
        print("Leitura Completa.")
        if(self.flag == 1):
            exit()
        else:
            return pos

    def consulta_tabela(self, posicao):
        """Retorna o elemento"""
        # print "Pos", posicao
        if(posicao >= len(self.lista)):
            posicao -= 1
        for i in range(posicao, -1, -1):
            for palavras in self.elemento:
                if(self.lista[i][0] in palavras):
                    return self.tabela[self.lista[i][2]][2].split(" ")[0], self.tabela[self.lista[i][2]][1]

    def erro(self, simb, pos):
        """Indica que ocorreu um erro"""
        print("Erro Caracter: " + simb)
        validos = ["LIT", "ID", "NUM", "int", "float", "char"]
        self.indica_erro = 1
        try:
            print("Linha: " + self.consulta_tabela(pos)[0])
            return pos
        except Exception as e:
            print("Linha: " + self.consulta_tabela(pos)[0])
        return pos

    def verica_declarado(self, simb):
        """Verifica se o simbolo já foi declarado"""
        if(simb not in self.elemento):
            simb = self.consulta_tabela(simb)[1]
        if(simb not in self.tabela_declaracao):
            print("Símbolo não declarado: " + simb)
            #self.erro("Símbolo Não declarado", simb,)
            return -1
        else:
            return 1

    def retorna_registrador(self, pos):
        """Retorna o registrador"""
        if(self.verica_declarado(pos) == 1):
            return self.tabela_declaracao[self.consulta_tabela(pos)[1]][2]

    def compara_tipo(self, tipo_a, tipo_b):
        """ Compara os tipos"""
        if(tipo_a != tipo_b):
            print("Erro - Tipos diferentes: " + tipo_a + ' e ' + tipo_b)
            self.erro("Tipos Diferentes", tipo_a)

    def verifica_tipos(self, tipo_a, tipo_b):
        """Verica se os tipos são compativeis"""
        if(tipo_a in self.elemento):
            retorno = tipo_a
        else:
            retorno = tipo_b
        if(tipo_a not in self.elemento):

            if(self.verica_declarado(tipo_a) == 1):
                tipo_a = self.tabela_declaracao[
                    self.consulta_tabela(tipo_a)[1]][0]
        if(tipo_b not in self.elemento):
            if(self.verica_declarado(tipo_b) == 1):
                tipo_b = self.tabela_declaracao[
                    self.consulta_tabela(tipo_b)[1]][0]
        if(tipo_a != tipo_b):
            print("Erro - Tipos diferentes: " + tipo_a + " e " + tipo_b)
            self.erro("Tipos Diferentes", retorno)
        else:
            return retorno

    def gera_codigo(self, opcao, pos, retorno_geracao):
        """Realiza a geração de código de C para Python"""
        arquivo = open("geracao", "a")
        self.cont += 1
        registrador = "$S" + str(self.cont)
        if(opcao == "+" or opcao == "-" or opcao == "*" or
             opcao == "/" or opcao == ">" or opcao == "<"):
            simb = self.retorna_registrador(pos - 2)
            simb2 = self.retorna_registrador(pos)
            tipo_retorno = self.verifica_tipos(pos - 2, pos)
            retorno_geracao = opcao + " " + registrador + \
                "," + str(simb) + "," + str(simb2)
            print(retorno_geracao)
            arquivo.write(retorno_geracao)
            arquivo.write('\n')
            return retorno_geracao, tipo_retorno
        arquivo.close()

    def programa(self):
        """Função programa"""
        # self.pos_global -= 1
        simb, pos = self.get_next_token(self.tokens, self.pos_global)
        # print "First PROG ", simb
        if(simb == "$"):
            """Final da leitura"""
            return self.valido(pos)
        elif(simb in self.tipo):
            """Válida uma declaração"""
            pos = self.declaracao(pos)
            simb = self.tokens[pos]
            if(simb not in " $ "):
                self.pos_global = pos
                return self.programa()
            elif(simb in " $ "):
                return self.valido(pos)
            if(simb not in " ; "):
                return self.erro(simb, pos)
        elif ("ID" in simb):
            """Válida uma Atribuição"""
            ret_pos = self.atribuicao(pos)
            sim, pos = self.get_next_token(self.tokens, ret_pos)
            if(simb in "$"):
                return self.valido
            self.pos_global = pos
            return self.programa()
        elif ("while" in simb):
            """Válida a estrutura de repetição while"""
            self.flag = 1
            ret_pos = self.repeticao(pos)
            self.pos_global = ret_pos
            self.programa()
        elif (simb in "if"):
            """Valida a estrutura condicional"""
            simb, pos = self.get_next_token(self.tokens, pos)
            self.gera_codigo("if", pos, 1)
            pos = self.condicional(pos)
            self.gera_codigo("return", pos, None)
        else:
            return pos

    def condicional(self, pos):
        """Valida uma condição"""
        simb = self.tokens[pos]
        pos = self.E(simb, self.tokens, pos)
        simb, pos = self.get_next_token(self.tokens, pos)
        if(simb in " { "):
            self.pos_global = pos
            pos = self.programa()
            pos = pos - 2
            simb = self.tokens[pos]
            if(simb in " } "):
                simb, pos = self.get_next_token(self.tokens, pos)
                if(simb in " ; "):
                    print("Condicional Correto")
                else:
                    self.erro(simb, pos)
                    return pos
        else:
            self.erro(simb, pos)
            return pos

    def declaracao_virgula(self, pos, tipo):
        """Válida declaração multipla"""
        simb, pos = self.get_next_token(self.tokens, pos)
        self.adiciona_tabela(pos, tipo)
        if("ID" in simb):
            self.gera_codigo("Load", pos, None) # a = 5
            simb, pos = self.get_next_token(self.tokens, pos)
            self.warning_inicializado(pos)
            if("," in simb):
                self.declaracao_virgula(pos)
            elif(";" in simb):
                return pos
            else:
                self.erro(simb, pos)
                return pos
        else:
            self.erro(simb, pos)
            return pos

    def atribuicao(self, pos):
        """Válida uma atribuicao"""
        simb = self.tokens[pos]
        pos_geracao = pos
        if("ID" in simb):
            simb, pos = self.get_next_token(self.tokens, pos)
            print('SIMB', simb)
            if("=" in simb):
                simb, pos = self.get_next_token(self.tokens, pos)
                try:
                    pos, retorno_geracao, tipo_retorno = self.E(
                        simb, self.tokens, pos)
                    self.gera_codigo("Store", pos_geracao, retorno_geracao) # a = b
                    self.verifica_tipos(tipo_retorno, pos_geracao)
                except Exception as e:
                    pos = self.E(simb, self.tokens, pos)
                else:
                    pass
                print("Atribuição Válida")
                simb, pos = self.get_next_token(self.tokens, pos)
                if(simb != ";" and simb != "$"):
                    self.pos_global = pos - 1
                    pos = self.programa()
                    return pos
                else:
                    return pos
            else:
                return self.erro(simb, pos)
        else:
            print("Símbolo"), simb
            return pos

    def adiciona_tabela(self, pos, tipo):
        """Verifica se o elemento já esta na tabela"""
        # print self.lista[pos], self.lista
        simb = self.lista[pos][1]
        linha = self.consulta_tabela(pos)
        if(simb in self.tabela_declaracao):
            print("Erro Simbolo: " + simb + ",Já declarado " + self.tabela_declaracao[simb][1])
            self.indica_erro = 1
        else:
            print("Adicionado na lista de símbolos")
            self.tabela_declaracao[simb] = [tipo, linha]

    def declaracao(self, pos):
        """Verifica a declaracao"""
        simb = self.tokens[pos]
        if(simb in self.tipo):
            """Verifica se simbolo é int, float ou char."""
            tipo = simb
            simb, pos = self.get_next_token(self.tokens, pos)
            # print simb
            if(simb in "ID"):
                # print self.tokens[pos - 1], self.lista[pos][1],
                # self.consulta_tabela(pos)
                self.adiciona_tabela(pos, tipo)
                self.gera_codigo("Load", pos, None)
                simb, pos = self.get_next_token(self.tokens, pos)

                if(simb == ";"):
                    print("Declaração Válida.")
                    self.warning_inicializado(pos)
                    return pos
                elif("," in simb):
                    return self.declaracao_virgula(pos, tipo)
                else:
                    pos -= 1
                    # print pos
                    valor = self.atribuicao(pos)
                    if(valor == None):
                        self.indica_erro = 1
                        exit()
                    return valor

    def repeticao(self, pos):
        """Define a estrutura de repeticao"""
        simb = self.tokens[pos]
        # print "while"
        print(simb)
        if(simb in "while"):
            self.gera_codigo("return", pos, None)
            simb, pos = self.get_next_token(self.tokens, pos)
            pos = self.E(simb, self.tokens, pos)

            simb, pos = self.get_next_token(self.tokens, pos)
            if(simb in "$"):
                print("Leitura Completa")
                return pos
            elif("{" in simb):
                simb, pos = self.get_next_token(self.tokens, pos)
                self.pos_global = pos
                self.gera_codigo("if", pos, 2)
                ret_pos = self.bloco()
                simb = self.tokens[ret_pos - 2]
                if("}" in simb):

                    simb, pos = self.get_next_token(self.tokens, ret_pos - 2)
                    if(";" in simb):
                        print("While válido")
                        return pos
                else:
                    print("Bloco")
                    self.gera_codigo("return", pos, None)
                    # print "erro"
                    ##self.erro(simb, pos)

    def bloco(self):
        """Bloco de programa"""
        return self.programa()

    def conector(self, lista, tabela):
        """Realiza a ponte de conexão entre o Analisador Léxico e o Sintático"""
        # print("Entrada Sintático "), lista
        # print(lista)
        self.lista = lista
        self.tabela = tabela
        cont = 0
        for i in lista:
            cont = cont + 1
            if(i[0] == "NUM" or i[0] == "LIT" or i[0] in "ID"):
                self.tokens.append(i[0])
            elif("RES" in i[0]):
                self.tokens.append(i[1])
            else:
                self.tokens.append(i[0])
        self.tokens.append("$")
        print("Entrada Sintático: "), self.tokens
        self.programa()
        if(self.indica_erro == 0 and self.warning == 0):
            print("Retorno sem erros")
        elif(self.warning == 1):
            print("Leitura Completa - Verifique os [WARNINGS]")
        else:
            print("Leitura Completa - Verifique os Erros")
            