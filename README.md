# Compilador

A linguagem de origem será a linguagem C adaptada/limitada. Para o compilador será utilizado Python e a linguagem de destino também será Python.

O caso que será utilizado como exemplo é o Algoritmo de Luhn, que serve para a validação de cartões de crédito. Esse algoritmo é capaz de detectar um erro simples em um dígito, assim como a maioria das transposições de um dígito com os dígitos adjacentes. 

Este algoritmo verifica se um número de cartão é bem formado realizando operações matemáticas simples. Note que passar no teste de Luhn quer simplesmente dizer que não ocorreram erros, ou seja, o número é bem formado.

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

## Representação Léxica

### Exemplo de algoritmo em C para análise léxica

```
#include <stdio.h>

int main()
{
    int pera = 3;
    char qualidade = 'A';
    float peso = 2.5 + 1;

    printf("Existem %d peras de qualidade %c ", pera, qualidade);
    printf("pesando %f quilos.\n", peso);
}
```

### Retorno da análise léxica

```
[['RES: 1', 'int', 6], ['ID', 'main', 11], ['('], [')'], ['{'], ['RES: 1', 'int', 23], ['ID', 'pera', 28], ['='], ['NUM', '3', 32], [';'], ['RES: 3', 'char', 42], ['ID', 'qualidade', 52], ['='], '[Token Inválido]', ['ID', 'A', 57], '[Token Inválido]', [';'], ['RES: 2', 'float', 69], ['ID', 'peso', 74], ['='], ['NUM', '2.5', 80], ['+'], ['NUM', '1', 84], [';'], ['RES: 6', 'printf', 97], ['('], ['LIT', '"Existem %d peras de qualidade %c "', 132], [','], ['ID', 'pera', 139], [','], ['ID', 'qualidade', 150], [')'], [';'], ['RES: 6', 'printf', 163], ['('], ['LIT', '"pesando %f quilos', 185], [','], ['ID', 'peso', 192], [')'], [';'], ['}']]
```

## Análise sintática: exemplo das gramáticas

### Declaração de variáveis

```
cardnum = “79927398713”
qtdigits = 12
sum = 0
carnum = [12]

S => COMANDO | $
COMANDO => <id> | <id><op><VALOR> | <id><op><EXPR> | <id><op><BLOCO>
EXPR => <id><op><id>
VALOR => <id> | <val> | <””> | <op><val> | <[]>
id => <LIT>
BLOCO => COMANDO

S
COMANDO
<id>
<id><op><id>
<id><op><val>
<id><op><””>
<id><op><op><val>
<id><op><[]>
<id><op><EXPR>
<id><op><id><op><id>
<id><op><BLOCO>
<id><op><id><op><EXPR>
<id><op><id><op><val>
```
### If e Else

```
if (sum % 10 == 0):
       print("Cartão válido")
else:
       print(“Cartao invalido”)

S => COMANDO | $
COMANDO => <if><(>EXPR<)><:>BLOCO<else><:><BLOCO> | <id><(><val><)>
EXPR => <id><op><val><op><val>
BLOCO => COMANDO

S
COMANDO
<if><(>EXPR<)><:>BLOCO<else><:>BLOCO
<if><(><id><op><val><op><val><)><:>BLOCO<else><:>BLOCO
<if><(><id><op><val><op><val><)><:>COMANDO<else><:>COMANDO
<if><(><id><op><val><op><val><)><:><id><(><val><)><else><:><id><(><val><)>
```

### For

```
for i in range(qtdigits - 1, -1, -2):
     d = ord(carnum[i]) - ord('0’)

S => COMANDO| $
COMANDO => <id><(><val><)> | <for><id><in><id><(>EXPR<)><:>BLOCO
EXPR => <id><val><,><val><,><val> | <id><[><val><]>
BLOCO => <id><op><id><(>EXPR<)><op>COMANDO

S
COMANDO
<for><id><in><id><(>EXPR<)><:>BLOCO
<for><id><in><id><(><id><val><,><val><,><val><)><:>BLOCO
<for><id><in><id><(><id><val><,><val><,><val><)><:><id><op><id><(>EXPR<)><op>COMANDO
<for><id><in><id><(><id><val><,><val><,><val><)><:><id><op><id><(><id><[><val><]><)><op>COMANDO
<for><id><in><id><(><id><val><,><val><,><val><)><:><id><op><id><(><id><[><val><]><)><op><id><(><val><)>
```

### While

```
while error > 1:
	error = error /4
	printf(error)

S => COMANDO| $
COMANDO => EXPR<id><(><val><)>
EXPR => <id><op><val> | <id><op><id><op><val>
BLOCO => COMANDO

S
COMANDO
<while>EXPR<:>BLOCO
<while><id><op><val><:>BLOCO
<while><id><op><val><:>COMANDO
<while><id><op><val><:>EXPR<id><(><val><)>
<while><id><op><val><:><id><op><id><op><val><id><(><val><)>
```

## First e Follow das gramáticas

```
PROGRAMA (S) => D|A|C|R|$
ATRIBUIÇÃO (A) => id = E;|S
DECLARAÇÃO (D) => T id;|T A;|S
TIPO (T) => int|float|char
REPETIÇÃO (R) => while(E){B};|for(E op id; E op id; E op){B};|S
EXPRESSÃO (E) => num|id|lit|””|(E);|S                                      (expressões aritméticas)
Condição -> if(E op E){B};|if(E op E){B}else{B};|if(E op E){B}else{B}elseif(E op E){B};|S
Bloco -> S|$
```

|   |   |   |   |   |
|---|---|---|---|---|
|First (S) = First (D) = FIRST T =  {int, float, char}  | Follow (S) = { $}|
|First A = { id, int}   | Follow A = {if, $}  |
|First R = {while, for, $}   | Follow D = {if, $}|   
|First E = {num, id, lit, “”, $}   |Follow T = {id}   |
|First C = {if, $} | Follow R = {$} |
|First B = {int, $} | Follow E = {if, $}|
| | Follow C = {while, $}| 
| | Follow B = {$}|
