
Pacote ``estrutarq.campo``
**************************

Implementação de organizações de campos.


Organização básica
==================

Implementação de campos.

Este arquivo provê a classe básica para definição de campos.

Uma classe básica `CampoBasico <#estrutarq.campo.CampoBasico>`_ define
uma classe abstrata (ABC) com as propriedades e métodos gerais. Dela
são derivados os demais campos. A classe `CampoBruto
<#estrutarq.campo.CampoBruto>`_ define um campo sem organização que
utiliza https://docs.python.org/3/library/stdtypes.html#str (UTF-8)
como valor.

``terminador_de_campo:
https://docs.python.org/3/library/stdtypes.html#bytes = b'\x00'``

    O terminador de campo é um byte único usado como delimitador para
    o fim do campo. O valor padrão é ``0x00``.


Campo básico
------------

Todas as demais classes do módulo são derivadas de uma classe básica.

**class CampoBasico(tipo: str)**

    Base: `estrutarq.dado.dado_comum.DadoBasico
    <Estrutarq.Dado#estrutarq.dado.DadoBasico>`_

    Classe básica para campo, a menor unidade de informação.

    :Parâmetros:
        **tipo** (https://docs.python.org/3/library/stdtypes.html#str)
        – cadeia de caracteres com o nome do tipo; possíveis valores
        são, por exemplo, ``"cadeia fixo"``, ``"real terminador"`` ou
        ``"int prefixado"``

    ``property tipo``

        Nome do campo, sendo um valor puramente ornamental (i.e., não
        é usado internamente com nenhum fim).

        :Tipo de retorno:
            https://docs.python.org/3/library/stdtypes.html#str

    ``abstract property valor``

        Valor do campo, usando sua representação interna.

    **abstract bytes_para_valor(dado: bytes)**

        Conversão de uma sequência de bytes para armazenamento para
        valor do campo, de acordo com a representação de dados. O
        `valor <#estrutarq.campo.CampoBasico.valor>`_ é atualizado.

        :Parâmetros:
            **dado**
            (https://docs.python.org/3/library/stdtypes.html#bytes) –
            sequência de bytes

    **abstract valor_para_bytes() ->
    https://docs.python.org/3/library/stdtypes.html#bytes**

        Conversão do valor do campo para sequência de bytes de acordo
        com a representação de dados.

        :Retorna:
            sequência de bytes

        :Tipo de retorno:
            https://docs.python.org/3/library/stdtypes.html#bytes

    **tem_comprimento_fixo() ->
    https://docs.python.org/3/library/functions.html#bool**

        Retorna se o comprimento é ou não fixo.

        :Retorna:
            *True* para comprimento fixo ou *False* para variável

        :Tipo de retorno:
            https://docs.python.org/3/library/functions.html#bool

    **comprimento() ->
    https://docs.python.org/3/library/functions.html#int**

        Obtém o comprimento atual do campo após convertido para
        sequência de bytes, o que inclui a organização do dado.

        :Retorna:
            o comprimento do campo com a organização

        :Tipo de retorno:
            https://docs.python.org/3/library/functions.html#int

    **leia(arquivo: BinaryIO)**

        Leitura da sequência de bytes que representa o campo e sua
        conversão para o valor do campo, obedecendo à organização e
        formato de representação. O `valor
        <#estrutarq.campo.CampoBasico.valor>`_ é atualizado.

        :Parâmetros:
            **arquivo** (*BinaryIO*) – arquivo binário aberto com
            permissão de leitura

    **escreva(arquivo: BinaryIO)**

        Conversão do valor do campo para sequência de bytes e
        armazenamento no arquivo, incluindo a organização de dados.

        :Parâmetros:
            **arquivo** (*BinaryIO*) – arquivo binário aberto com
            permissão de escrita

    **copy()**

        Cópia “rasa” do objeto.

        :Retorna:
            uma instância copiada de ``self``


Campo bruto
-----------

**class CampoBruto(valor='')**

    Base: `estrutarq.dado.dado_comum.DadoBruto
    <Estrutarq.Dado#estrutarq.dado.DadoBruto>`_,
    `estrutarq.campo.campo_comum.CampoBasico
    <#estrutarq.campo.CampoBasico>`_

    Implementação das funções de um campo bruto, ou seja, sem
    organização de campo. O valor é sempre armazenado como cadeia de
    caracteres com codificação de caracteres UTF-8.

    :Parâmetros:
        **valor**
        (https://docs.python.org/3/library/stdtypes.html#str*,
        **opcional*) – valor do campo

    ``property valor:
    https://docs.python.org/3/library/stdtypes.html#str``

        O valor armazenado no campo (cadeia de caracteres).

        :Retorna:
            o valor do campo

        :Tipo de retorno:
            https://docs.python.org/3/library/stdtypes.html#str

    **bytes_para_valor(dado: bytes)**

        Atualização do valor do campo a partir de uma sequência de
        bytes com codificação UTF-8.

        :Parâmetros:
            **dado**
            (https://docs.python.org/3/library/stdtypes.html#bytes) –
            a sequência de bytes

    **valor_para_bytes() ->
    https://docs.python.org/3/library/stdtypes.html#bytes**

        Retorno do valor do campo (cadeia de caracteres) convertido
        para uma sequência de bytes, usando codificação UTF-8.

        :Retorna:
            a sequência de bytes

        :Tipo de retorno:
            https://docs.python.org/3/library/stdtypes.html#bytes


Cadeias de caracteres
=====================

Campos para armazenamento de cadeias de caracteres.

Este arquivo provê classes para uso de campos cujo conteúdo é uma
cadeia de caracteres. Internamente, o tipo
https://docs.python.org/3/library/stdtypes.html#str é usado para
armazenamento e a transformação para sequência de bytes usa a
codificação UTF-8.

Uma classe básica ``CampoCadeiaBasico`` define uma classe abstrata
(ABC) com as propriedades e métodos gerais. Dela são derivados campos:

*   Com terminador

*   Prefixado pelo comprimento

*   De comprimento fixo predefinido


Campo cadeia básico
-------------------

**class CampoCadeiaBasico(tipo: str, valor: str = '')**

    Base: `estrutarq.campo.campo_comum.CampoBasico
    <#estrutarq.campo.CampoBasico>`_

    Classe básica para cadeias de caracteres.

    :Parâmetros:
        *   **tipo**
            (https://docs.python.org/3/library/stdtypes.html#str) –
            nome do tipo (definido nas subclasses)

        *   **valor**
            (https://docs.python.org/3/library/stdtypes.html#str*,
            **opcional*) – o valor a ser armazenado no campo (padrão:
            ``""``)

    ``property valor``

        Valor do campo, usando sua representação interna.

    **bytes_para_valor(dado: bytes)**

        Armazenamento da sequência de bytes de ``dado`` como valor do
        campo.

        :Parâmetros:
            **dado**
            (https://docs.python.org/3/library/stdtypes.html#bytes) –
            sequência de bytes com codificação UTF-8

    **valor_para_bytes() ->
    https://docs.python.org/3/library/stdtypes.html#bytes**

        Retorno do valor do campo convertido para sequência de bytes
        usando codificação UTF-8.

        :Retorna:
            sequência de bytes

        :Tipo de retorno:
            https://docs.python.org/3/library/stdtypes.html#bytes


Campo cadeia com terminador
---------------------------

**class CampoCadeiaTerminador(**kwargs)**

    Base: `estrutarq.dado.dado_comum.DadoTerminador
    <Estrutarq.Dado#estrutarq.dado.DadoTerminador>`_,
    `estrutarq.campo.campo_cadeia.CampoCadeiaBasico
    <#estrutarq.campo.CampoCadeiaBasico>`_

    Classe para cadeia de caracteres com terminador. O terminador de
    campo é definido por ``estrutarq.campo.terminador_de_campo``.

    :Parâmetros:
        **kwargs**
        (https://docs.python.org/3/library/stdtypes.html#dict*,
        **opcional*) – lista de parâmetros opcionais passados para
        ``CampoCadeiaBasico``


Campo cadeia prefixado pelo comprimento
---------------------------------------

**class CampoCadeiaPrefixado(**kwargs)**

    Base: `estrutarq.dado.dado_comum.DadoPrefixado
    <Estrutarq.Dado#estrutarq.dado.DadoPrefixado>`_,
    `estrutarq.campo.campo_cadeia.CampoCadeiaBasico
    <#estrutarq.campo.CampoCadeiaBasico>`_

    Classe para cadeia de caracteres prefixada pelo comprimento. O
    prefixo é o adotado em `DadoPrefixado
    <Estrutarq.Dado#estrutarq.dado.DadoPrefixado>`_.

    :Parâmetros:
        **kwargs**
        (https://docs.python.org/3/library/stdtypes.html#dict*,
        **opcional*) – lista de parâmetros opcionais passados para
        `CampoCadeiaBasico <#estrutarq.campo.CampoCadeiaBasico>`_


Campo cadeia de comprimento fixo
--------------------------------

**class CampoCadeiaFixo(comprimento: int, **kwargs)**

    Base: `estrutarq.dado.dado_comum.DadoFixo
    <Estrutarq.Dado#estrutarq.dado.DadoFixo>`_,
    `estrutarq.campo.campo_cadeia.CampoCadeiaBasico
    <#estrutarq.campo.CampoCadeiaBasico>`_

    Classe para cadeia de caracteres com comprimento fixo, com
    enchimento de bytes e preenchimento de bytes inválidos. O byte de
    prenchimento é o padrão de `DadoFixo
    <Estrutarq.Dado#estrutarq.dado.DadoFixo>`_.

    :Parâmetros:
        *   **comprimento**
            (https://docs.python.org/3/library/functions.html#int) – o
            comprimento do campo em bytes

        *   **kwargs**
            (https://docs.python.org/3/library/stdtypes.html#dict*,
            **opcional*) – lista de parâmetros opcionais passados para
            `CampoCadeiaBasico <#estrutarq.campo.CampoCadeiaBasico>`_


Valores inteiros
================

Campos para armazenamento de valores inteiros.

Este arquivo provê classes para uso de campos cujo conteúdo é um valor
inteiro com sinal. Internamente, o tipo
https://docs.python.org/3/library/functions.html#int é usado para
armazenamento e a transformação para sequência de bytes podem ser
textuais ou binária.

Uma classe básica `CampoIntBasico
<#estrutarq.campo.campo_inteiro.CampoIntBasico>`_ define uma classe
abstrata (ABC) com as propriedades e métodos gerais. Dela são
derivados campos:

*   Com terminador

*   Prefixado pelo comprimento

*   Binário

*   De comprimento fixo predefinido


Campo inteiro básico
--------------------

**class CampoIntBasico(tipo: str, valor: int = 0)**

    Base: `estrutarq.campo.campo_comum.CampoBasico
    <#estrutarq.campo.CampoBasico>`_

    Classe básica para campo inteiro.

    :Parâmetros:
        *   **tipo**
            (https://docs.python.org/3/library/stdtypes.html#str) – o
            nome do tipo (definido em subclasses)

        *   **valor**
            (https://docs.python.org/3/library/functions.html#int*,
            **opcional*) – o valor a ser armazenado no campo (padrão:
            0)

    ``property valor:
    https://docs.python.org/3/library/functions.html#int``

        Valor inteiro armazenado no campo.

    **bytes_para_valor(dado: bytes)**

        Conversão de uma sequência de bytes (representação textual)
        para inteiro :param dado: sequência de bytes

    **valor_para_bytes() ->
    https://docs.python.org/3/library/stdtypes.html#bytes**

        Conversão do valor inteiro para sequência de bytes usando
        representação textual e codificação UTF-8 :return: sequência
        de bytes


Campo inteiro com terminador
----------------------------

**class CampoIntTerminador(terminador: bytes = b'\x00', **kwargs)**

    Base: `estrutarq.dado.dado_comum.DadoTerminador
    <Estrutarq.Dado#estrutarq.dado.DadoTerminador>`_,
    `estrutarq.campo.campo_inteiro.CampoIntBasico
    <#estrutarq.campo.campo_inteiro.CampoIntBasico>`_

    Classe para inteiro textual com terminador


Campo inteiro prefixado pelo comprimento
----------------------------------------

**class CampoIntPrefixado(**kwargs)**

    Base: `estrutarq.dado.dado_comum.DadoPrefixado
    <Estrutarq.Dado#estrutarq.dado.DadoPrefixado>`_,
    `estrutarq.campo.campo_inteiro.CampoIntBasico
    <#estrutarq.campo.campo_inteiro.CampoIntBasico>`_

    Classe para inteiro textual com prefixo de comprimento_bloco


Campo inteiro binário
---------------------

**class CampoIntBinario(**kwargs)**

    Base: `estrutarq.dado.dado_comum.DadoBinario
    <Estrutarq.Dado#estrutarq.dado.DadoBinario>`_,
    `estrutarq.campo.campo_inteiro.CampoIntBasico
    <#estrutarq.campo.campo_inteiro.CampoIntBasico>`_

    Classe para inteiro em formato binário (big endian) com 8 bytes e
    complemento para 2 para valores negativos

    ``numero_bytes = 8``

    **bytes_para_valor(dado: bytes)**

        Conversão de uma sequência de bytes (binária big-endian com
        sinal) para inteiro :param dado: sequência de bytes

    **valor_para_bytes() ->
    https://docs.python.org/3/library/stdtypes.html#bytes**

        Conversão do valor inteiro para sequência de bytes usando
        representação binária big-endian com sinal :return: sequência
        de bytes


Campo inteiro de comprimento fixo
---------------------------------

**class CampoIntFixo(comprimento: int, **kwargs)**

    Base: `estrutarq.dado.dado_comum.DadoFixo
    <Estrutarq.Dado#estrutarq.dado.DadoFixo>`_,
    `estrutarq.campo.campo_inteiro.CampoIntBasico
    <#estrutarq.campo.campo_inteiro.CampoIntBasico>`_

    Classe para inteiro textual com tamanho fixo


Valores reais
=============


Campo real básico
-----------------

**class CampoRealBasico(tipo: str, valor: float = 0)**

    Base: `estrutarq.campo.campo_comum.CampoBasico
    <#estrutarq.campo.CampoBasico>`_

    Classe básica para campo real

    ``property valor:
    https://docs.python.org/3/library/functions.html#float``

        Valor do campo, usando sua representação interna.

    **bytes_para_valor(dado: bytes)**

        Conversão de sequência de bytes com valor textual para valor
        real :param dado: sequência de 8 bytes

    **valor_para_bytes() ->
    https://docs.python.org/3/library/stdtypes.html#bytes**

        Conversão do valor do campo para sequência de bytes textual
        :return: a sequência de bytes no padrão especificado


Campo real com terminador
-------------------------

**class CampoRealTerminador(terminador: bytes = b'\x00', **kwargs)**

    Base: `estrutarq.dado.dado_comum.DadoTerminador
    <Estrutarq.Dado#estrutarq.dado.DadoTerminador>`_,
    `estrutarq.campo.campo_real.CampoRealBasico
    <#estrutarq.campo.campo_real.CampoRealBasico>`_

    Classe para campo real com representação textual de
    comprimento_bloco fixo


Campo real prefixado pelo comprimento
-------------------------------------

**class CampoRealPrefixado(**kwargs)**

    Base: `estrutarq.dado.dado_comum.DadoPrefixado
    <Estrutarq.Dado#estrutarq.dado.DadoPrefixado>`_,
    `estrutarq.campo.campo_real.CampoRealBasico
    <#estrutarq.campo.campo_real.CampoRealBasico>`_

    Classe para campo real com representação textual de
    comprimento_bloco fixo


Campo real binário
------------------

**class CampoRealBinario(**kwargs)**

    Base: `estrutarq.dado.dado_comum.DadoBinario
    <Estrutarq.Dado#estrutarq.dado.DadoBinario>`_,
    `estrutarq.campo.campo_real.CampoRealBasico
    <#estrutarq.campo.campo_real.CampoRealBasico>`_

    Classe para real em formato binário usando IEEE 754 de precisão
    dupla

    **bytes_para_valor(dado: bytes)**

        Conversão de sequência de bytes com representação IEEE 754 de
        precisão dupla para real :param dado: sequência de 8 bytes

    **valor_para_bytes() ->
    https://docs.python.org/3/library/stdtypes.html#bytes**

        Conversão do valor do campo para sequência de bytes no padrão
        IEEE 754 de precisão dupla :return: a sequência de bytes no
        padrão especificado


Campo real de comprimento fixo
------------------------------

**class CampoRealFixo(comprimento: int, **kwargs)**

    Base: `estrutarq.dado.dado_comum.DadoFixo
    <Estrutarq.Dado#estrutarq.dado.DadoFixo>`_,
    `estrutarq.campo.campo_real.CampoRealBasico
    <#estrutarq.campo.campo_real.CampoRealBasico>`_

    Classe para campo real com representação textual de
    comprimento_bloco fixo
