# Compilador

A linguagem de origem será a linguagem C adaptada/limitada. Para o compilador será utilizado Python e a linguagem de destino também será Python.

## Integrantes

* Bruno Rocha - 161046
* Gal Bronstein - 160870
* João Almeida - 120693
* Karine Pistili - 171469
* Lucas Capucho - 153533

## Funcionalidades da liguagem origem

- As palavras reservadas da linguagem e que podem ser lidas pelas instruções são: 

['int', 'float', 'char', 'if', 'else', 'printf', 'for', 'while', 'return', 'continue', 'break', 'read']

- Os separadores definidos: 

[';', '[', ']', ')', '(', ')', '{', '}', ',', '=', '.']

- Os operadores aritméticos:

['-', '+', '/', '*', '^', '%'] e ['++', '--', '==', '&&', '||', '<=', '>=', '!=']

- Possui variáveis e constantes;
- Operadores aritméticos;
- Instruções condicionais e blocos de repetição (if, else-if, else, for, break, continue);
- Não inclui recursos de orientação a objeto;
- Não inclui construção de funções e suporte a recursão;
- Não trata inclusão de bibliotecas;
- Não tem suporte ao tipo boolean, usa 0 ou 1 no lugar;
- O tipo char da linguagem trabalha como uma string, podendo ter mais de 1 caractere;
- O símbolo '^’ trabalha como o operador !, invertendo 0 para 1 ou vice-versa;

## Especificação das regras para obtenção de símbolos léxicos

<RES> para palavras reservadas
<ID> para identificadores
<NUM> para constantes numéricas
<LIT> para literal
<'{'> para separadores
<'+'> para operadores
