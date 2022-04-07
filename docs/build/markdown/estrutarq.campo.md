# Pacote `estrutarq.campo`

Implementação de organizações de campos.

<!-- Licença: GNU GENERAL PUBLIC LICENSE V.3, 2007
Jander Moreira, 2021-2022 -->
## Organização básica

Implementação de campos.

Este arquivo provê a classe básica para definição de campos.

Uma classe básica `CampoBasico`
define uma classe abstrata (ABC) com as propriedades e métodos gerais.
Dela são derivados os demais campos. A classe
`CampoBruto` define um
campo sem organização que utiliza [`str`](https://docs.python.org/3/library/stdtypes.html#str) (UTF-8) como valor.

<!-- Licença: GNU GENERAL PUBLIC LICENSE V.3, 2007
Jander Moreira, 2021-2022 -->

### terminador_de_campo(_: [bytes](https://docs.python.org/3/library/stdtypes.html#bytes_ _ = b'\\x00_ )
O terminador de campo é um byte único usado como delimitador para o
fim do campo. O valor padrão é `0x00`.

### Campo básico

Todas as demais classes do módulo são derivadas de uma classe básica.


### _class_ CampoBasico(tipo: [str](https://docs.python.org/3/library/stdtypes.html#str))
Base: [`estrutarq.dado.dado_comum.DadoBasico`](estrutarq.dado.md#estrutarq.dado.DadoBasico)

Classe básica para campo, a menor unidade de informação.


* **Parâmetros**

    **tipo** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – cadeia de caracteres com o nome do tipo; possíveis valores
    são, por exemplo, `"cadeia fixo"`, `"real terminador"` ou
    `"int prefixado"`



#### _property_ tipo()
Nome do campo, sendo um valor puramente ornamental (i.e., não é usado
internamente com nenhum fim).


* **Tipo de retorno**

    [str](https://docs.python.org/3/library/stdtypes.html#str)



#### _abstract property_ valor()
Valor do campo, usando sua representação interna.


#### _abstract_ bytes_para_valor(dado: [bytes](https://docs.python.org/3/library/stdtypes.html#bytes))
Conversão de uma sequência de bytes para armazenamento para valor
do campo, de acordo com a representação de dados.
O `valor` é atualizado.


* **Parâmetros**

    **dado** ([*bytes*](https://docs.python.org/3/library/stdtypes.html#bytes)) – sequência de bytes



#### _abstract_ valor_para_bytes()
Conversão do valor do campo para sequência de bytes de acordo
com a representação de dados.


* **Retorna**

    sequência de bytes



* **Tipo de retorno**

    [bytes](https://docs.python.org/3/library/stdtypes.html#bytes)



#### tem_comprimento_fixo()
Retorna se o comprimento é ou não fixo.


* **Retorna**

    True para comprimento fixo ou False para variável



* **Tipo de retorno**

    [bool](https://docs.python.org/3/library/functions.html#bool)



#### comprimento()
Obtém o comprimento atual do campo após convertido para sequência de
bytes, o que inclui a organização do dado.


* **Retorna**

    o comprimento do campo com a organização



* **Tipo de retorno**

    [int](https://docs.python.org/3/library/functions.html#int)



#### leia(arquivo: [BinaryIO](https://docs.python.org/3/library/typing.html#typing.BinaryIO))
Leitura da sequência de bytes que representa o campo e sua conversão
para o valor do campo, obedecendo à organização e formato de
representação.
O `valor` é atualizado.


* **Parâmetros**

    **arquivo** (*BinaryIO*) – arquivo binário aberto com permissão de leitura



#### escreva(arquivo: [BinaryIO](https://docs.python.org/3/library/typing.html#typing.BinaryIO))
Conversão do valor do campo para sequência de bytes e armazenamento no
arquivo, incluindo a organização de dados.


* **Parâmetros**

    **arquivo** (*BinaryIO*) – arquivo binário aberto com permissão de escrita



#### copy()
Cópia “rasa” do objeto.


* **Retorna**

    uma instância copiada de `self`


### Campo bruto


### _class_ CampoBruto(valor='')
Base: [`estrutarq.dado.dado_comum.DadoBruto`](estrutarq.dado.md#estrutarq.dado.DadoBruto), `estrutarq.campo.campo_comum.CampoBasico`

Implementação das funções de um campo bruto, ou seja, sem organização
de campo. O valor é sempre armazenado como cadeia de caracteres com
codificação de caracteres UTF-8.


* **Parâmetros**

    **valor** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)*, **opcional*) – valor do campo



#### _property_ valor(_: [str](https://docs.python.org/3/library/stdtypes.html#str_ )
O valor armazenado no campo (cadeia de caracteres).


* **Retorna**

    o valor do campo



* **Tipo de retorno**

    [str](https://docs.python.org/3/library/stdtypes.html#str)



#### bytes_para_valor(dado: [bytes](https://docs.python.org/3/library/stdtypes.html#bytes))
Atualização do valor do campo a partir de uma sequência de bytes
com codificação UTF-8.


* **Parâmetros**

    **dado** ([*bytes*](https://docs.python.org/3/library/stdtypes.html#bytes)) – a sequência de bytes



#### valor_para_bytes()
Retorno do valor do campo (cadeia de caracteres) convertido para uma
sequência de bytes, usando codificação UTF-8.


* **Retorna**

    a sequência de bytes



* **Tipo de retorno**

    [bytes](https://docs.python.org/3/library/stdtypes.html#bytes)


## Cadeias de caracteres

Campos para armazenamento de cadeias de caracteres.

Este arquivo provê classes para uso de campos cujo conteúdo é
uma cadeia de caracteres. Internamente, o tipo [`str`](https://docs.python.org/3/library/stdtypes.html#str) é usado
para armazenamento e a transformação para sequência de bytes
usa a codificação UTF-8.

Uma classe básica `CampoCadeiaBasico`
define uma classe abstrata (ABC) com as propriedades e métodos gerais. Dela
são derivados campos:


* Com terminador


* Prefixado pelo comprimento


* De comprimento fixo predefinido

<!-- Licença: GNU GENERAL PUBLIC LICENSE V.3, 2007
Jander Moreira, 2021-2022 -->
### Campo cadeia básico


### _class_ CampoCadeiaBasico(tipo: [str](https://docs.python.org/3/library/stdtypes.html#str), valor: [str](https://docs.python.org/3/library/stdtypes.html#str) = '')
Base: `estrutarq.campo.campo_comum.CampoBasico`

Classe básica para cadeias de caracteres.


* **Parâmetros**

    
    * **tipo** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – nome do tipo (definido nas subclasses)


    * **valor** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)*, **opcional*) – o valor a ser armazenado no campo
    (padrão: `""`)



#### _property_ valor()
Valor do campo, usando sua representação interna.


#### bytes_para_valor(dado: [bytes](https://docs.python.org/3/library/stdtypes.html#bytes))
Armazenamento da sequência de bytes de `dado` como valor
do campo.


* **Parâmetros**

    **dado** ([*bytes*](https://docs.python.org/3/library/stdtypes.html#bytes)) – sequência de bytes com codificação UTF-8



#### valor_para_bytes()
Retorno do valor do campo convertido para sequência
de bytes usando codificação UTF-8.


* **Retorna**

    sequência de bytes



* **Tipo de retorno**

    [bytes](https://docs.python.org/3/library/stdtypes.html#bytes)


### Campo cadeia com terminador


### _class_ CampoCadeiaTerminador(\*\*kwargs)
Base: [`estrutarq.dado.dado_comum.DadoTerminador`](estrutarq.dado.md#estrutarq.dado.DadoTerminador), `estrutarq.campo.campo_cadeia.CampoCadeiaBasico`

Classe para cadeia de caracteres com terminador. O terminador de campo é
definido por `estrutarq.campo.terminador_de_campo`.


* **Parâmetros**

    **kwargs** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)*, **opcional*) – lista de parâmetros opcionais passados para
    `CampoCadeiaBasico`


### Campo cadeia prefixado pelo comprimento


### _class_ CampoCadeiaPrefixado(\*\*kwargs)
Base: [`estrutarq.dado.dado_comum.DadoPrefixado`](estrutarq.dado.md#estrutarq.dado.DadoPrefixado), `estrutarq.campo.campo_cadeia.CampoCadeiaBasico`

Classe para cadeia de caracteres prefixada pelo comprimento. O prefixo é
o adotado em
[`DadoPrefixado`](estrutarq.dado.md#estrutarq.dado.DadoPrefixado).


* **Parâmetros**

    **kwargs** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)*, **opcional*) – lista de parâmetros opcionais passados para
    `CampoCadeiaBasico`


### Campo cadeia de comprimento fixo


### _class_ CampoCadeiaFixo(comprimento: [int](https://docs.python.org/3/library/functions.html#int), \*\*kwargs)
Base: [`estrutarq.dado.dado_comum.DadoFixo`](estrutarq.dado.md#estrutarq.dado.DadoFixo), `estrutarq.campo.campo_cadeia.CampoCadeiaBasico`

Classe para cadeia de caracteres com comprimento fixo, com enchimento de
bytes e preenchimento de bytes inválidos. O byte de prenchimento é o
padrão de [`DadoFixo`](estrutarq.dado.md#estrutarq.dado.DadoFixo).


* **Parâmetros**

    
    * **comprimento** ([*int*](https://docs.python.org/3/library/functions.html#int)) – o comprimento do campo em bytes


    * **kwargs** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)*, **opcional*) – lista de parâmetros opcionais passados para
    `CampoCadeiaBasico`


## Valores inteiros

Campos para armazenamento de valores inteiros.

Este arquivo provê classes para uso de campos cujo conteúdo é
um valor inteiro com sinal. Internamente, o tipo [`int`](https://docs.python.org/3/library/functions.html#int) é usado
para armazenamento e a transformação para sequência de bytes podem ser
textuais ou binária.

Uma classe básica `CampoIntBasico`
define uma classe abstrata (ABC) com as propriedades e métodos gerais.
Dela são derivados campos:


* Com terminador


* Prefixado pelo comprimento


* Binário


* De comprimento fixo predefinido

<!-- Licença: GNU GENERAL PUBLIC LICENSE V.3, 2007
Jander Moreira, 2021-2022 -->
### Campo inteiro básico


### _class_ CampoIntBasico(tipo: [str](https://docs.python.org/3/library/stdtypes.html#str), valor: [int](https://docs.python.org/3/library/functions.html#int) = 0)
Base: `estrutarq.campo.campo_comum.CampoBasico`

Classe básica para campo inteiro.


* **Parâmetros**

    
    * **tipo** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – o nome do tipo (definido em subclasses)


    * **valor** ([*int*](https://docs.python.org/3/library/functions.html#int)*, **opcional*) – o valor a ser armazenado no campo
    (padrão: 0)



#### _property_ valor(_: [int](https://docs.python.org/3/library/functions.html#int_ )
Valor inteiro armazenado no campo.


#### bytes_para_valor(dado: [bytes](https://docs.python.org/3/library/stdtypes.html#bytes))
Conversão de uma sequência de bytes (representação textual)
para inteiro
:param dado: sequência de bytes


#### valor_para_bytes()
Conversão do valor inteiro para sequência de bytes usando
representação textual e codificação UTF-8
:return: sequência de bytes

### Campo inteiro com terminador


### _class_ CampoIntTerminador(terminador: [bytes](https://docs.python.org/3/library/stdtypes.html#bytes) = b'\\x00', \*\*kwargs)
Base: [`estrutarq.dado.dado_comum.DadoTerminador`](estrutarq.dado.md#estrutarq.dado.DadoTerminador), `estrutarq.campo.campo_inteiro.CampoIntBasico`

Classe para inteiro textual com terminador

### Campo inteiro prefixado pelo comprimento


### _class_ CampoIntPrefixado(\*\*kwargs)
Base: [`estrutarq.dado.dado_comum.DadoPrefixado`](estrutarq.dado.md#estrutarq.dado.DadoPrefixado), `estrutarq.campo.campo_inteiro.CampoIntBasico`

Classe para inteiro textual com prefixo de comprimento_bloco

### Campo inteiro binário


### _class_ CampoIntBinario(\*\*kwargs)
Base: [`estrutarq.dado.dado_comum.DadoBinario`](estrutarq.dado.md#estrutarq.dado.DadoBinario), `estrutarq.campo.campo_inteiro.CampoIntBasico`

Classe para inteiro em formato binário (big endian) com 8 bytes
e complemento para 2 para valores negativos


#### numero_bytes(_ = _ )

#### bytes_para_valor(dado: [bytes](https://docs.python.org/3/library/stdtypes.html#bytes))
Conversão de uma sequência de bytes (binária big-endian com sinal)
para inteiro
:param dado: sequência de bytes


#### valor_para_bytes()
Conversão do valor inteiro para sequência de bytes usando
representação binária big-endian com sinal
:return: sequência de bytes

### Campo inteiro de comprimento fixo


### _class_ CampoIntFixo(comprimento: [int](https://docs.python.org/3/library/functions.html#int), \*\*kwargs)
Base: [`estrutarq.dado.dado_comum.DadoFixo`](estrutarq.dado.md#estrutarq.dado.DadoFixo), `estrutarq.campo.campo_inteiro.CampoIntBasico`

Classe para inteiro textual com tamanho fixo

## Valores reais

### Campo real básico


### _class_ CampoRealBasico(tipo: [str](https://docs.python.org/3/library/stdtypes.html#str), valor: [float](https://docs.python.org/3/library/functions.html#float) = 0)
Base: `estrutarq.campo.campo_comum.CampoBasico`

Classe básica para campo real


#### _property_ valor(_: [float](https://docs.python.org/3/library/functions.html#float_ )
Valor do campo, usando sua representação interna.


#### bytes_para_valor(dado: [bytes](https://docs.python.org/3/library/stdtypes.html#bytes))
Conversão de sequência de bytes com valor textual para valor real
:param dado: sequência de 8 bytes


#### valor_para_bytes()
Conversão do valor do campo para sequência de bytes textual
:return: a sequência de bytes no padrão especificado

### Campo real com terminador


### _class_ CampoRealTerminador(terminador: [bytes](https://docs.python.org/3/library/stdtypes.html#bytes) = b'\\x00', \*\*kwargs)
Base: [`estrutarq.dado.dado_comum.DadoTerminador`](estrutarq.dado.md#estrutarq.dado.DadoTerminador), `estrutarq.campo.campo_real.CampoRealBasico`

Classe para campo real com representação textual de comprimento_bloco fixo

### Campo real prefixado pelo comprimento


### _class_ CampoRealPrefixado(\*\*kwargs)
Base: [`estrutarq.dado.dado_comum.DadoPrefixado`](estrutarq.dado.md#estrutarq.dado.DadoPrefixado), `estrutarq.campo.campo_real.CampoRealBasico`

Classe para campo real com representação textual de comprimento_bloco fixo

### Campo real binário


### _class_ CampoRealBinario(\*\*kwargs)
Base: [`estrutarq.dado.dado_comum.DadoBinario`](estrutarq.dado.md#estrutarq.dado.DadoBinario), `estrutarq.campo.campo_real.CampoRealBasico`

Classe para real em formato binário usando IEEE 754 de precisão dupla


#### bytes_para_valor(dado: [bytes](https://docs.python.org/3/library/stdtypes.html#bytes))
Conversão de sequência de bytes com representação IEEE 754 de
precisão dupla para real
:param dado: sequência de 8 bytes


#### valor_para_bytes()
Conversão do valor do campo para sequência de bytes no padrão
IEEE 754 de precisão dupla
:return: a sequência de bytes no padrão especificado

### Campo real de comprimento fixo


### _class_ CampoRealFixo(comprimento: [int](https://docs.python.org/3/library/functions.html#int), \*\*kwargs)
Base: [`estrutarq.dado.dado_comum.DadoFixo`](estrutarq.dado.md#estrutarq.dado.DadoFixo), `estrutarq.campo.campo_real.CampoRealBasico`

Classe para campo real com representação textual de comprimento_bloco fixo
