
Pacote ``estrutarq.campo``
**************************


Módulo ``campo_comum``
======================

``estrutarq.comap.campo_comum``


Campo básico
------------

Todas as demais classes do módulo são derivadas de uma classe básica.

**class estrutarq.campo.CampoBasico(tipo: str)**

    Base: `estrutarq.dado.dado_comum.DadoBasico
    <Estrutarq.Dado#estrutarq.dado.DadoBasico>`_

    Estruturação básica do campo como menor unidade de informação.

    :Parâmetros:
        **tipo** (https://docs.python.org/3/library/stdtypes.html#str)
        – cadeia de caracteres com o nome do tipo

    **abstract bytes_para_valor(dado: bytes)**

        Conversão de uma sequência de bytes para armazenamento no
        valor do campo, de acordo com a representação de dados :param
        dado: sequência de bytes :return: o valor do campo de acordo
        com seu tipo

    **comprimento()**

        Obtém o comprimento atual do campo

        :Retorna:
            o comprimento do campo

    **comprimento_fixo()**

        Retorna se o comprimento é ou não fixo

        :Retorna:
            *True* para comprimento fixo ou *False* para variável

    **copy()**

        Cópia “rasa” deste campo :return: outra instância com os
        mesmos valores

    **escreva(arquivo: BinaryIO)**

        Conversão do valor para sequência de bytes e armazenamento no
        arquivo

        :Parâmetros:
            **arquivo** – arquivo binário aberto com permissão de
            escrita

    **leia(arquivo: BinaryIO)**

        Conversão dos dado lidos para o valor do campo, obedecendo à
        organização e formato de representação

        :Parâmetros:
            **arquivo** – arquivo binário aberto com permissão de
            leitura

    ``property tipo``

    ``abstract property valor``

        Recuperação, com as devidas conversões, do atributo
        ``__valor`` :return: o valor de ``__valor``

    **abstract valor_para_bytes() ->
    https://docs.python.org/3/library/stdtypes.html#bytes**

        Conversão do valor do campo para sequência de bytes de acordo
        com a representação de dados :return:


Módulo ``campo_cadeia``
=======================

``estrutarq.campo.campo_cadeia``

Campos para armazenamento de cadeias de caracteres.

Este arquivo provê classes para uso de campos cujo conteúdo é uma
cadeia de caracteres. Internamente, o tipo *str* é usado para
armazenamento e a transformação para sequência de bytes usa a
codificação UTF-8.

Uma classe básica `CampoCadeiaBasico
<#estrutarq.campo.CampoCadeiaBasico>`_ define uma classe abstrata
(ABC) com as propriedades e métodos gerais. Dela são derivados campos:

*   Com terminador

*   Prefixado pelo comprimento

*   De comprimento fixo predefinido


Campo cadeia básico
-------------------

**class estrutarq.campo.CampoCadeiaBasico(tipo: str, valor: str =
'')**

    Base: `estrutarq.campo.campo_comum.CampoBasico
    <#estrutarq.campo.CampoBasico>`_

    Classe básica para cadeias de caracteres.

    :Parâmetros:
        *   **tipo**
            (https://docs.python.org/3/library/stdtypes.html#str) –
            nome do tipo (definido nas classes derivadas)

        *   **valor**
            (https://docs.python.org/3/library/stdtypes.html#str*,
            **opcional*) – o valor a ser armazenado no campo (padrão:
            ``""``)

    **bytes_para_valor(dado: bytes)**

        Armazenamento da sequência de bytes de ``dado`` como valor do
        campo.

        :Parâmetros:
            **dado**
            (https://docs.python.org/3/library/stdtypes.html#bytes) –
            sequência de bytes com codificação UTF-8

    ``property valor``

        Recuperação, com as devidas conversões, do atributo
        ``__valor`` :return: o valor de ``__valor``

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

**class estrutarq.campo.CampoCadeiaTerminador(**kwargs)**

    Base: `estrutarq.dado.dado_comum.DadoTerminador
    <Estrutarq.Dado#estrutarq.dado.DadoTerminador>`_,
    `estrutarq.campo.campo_cadeia.CampoCadeiaBasico
    <#estrutarq.campo.CampoCadeiaBasico>`_

    Classe para cadeia de caracteres com terminador

    :Parâmetros:
        **kwargs** (*:class:dict*) – parâmetros nomeados a serem
        repassados


Campo cadeia prefixado pelo comprimento
---------------------------------------

**class estrutarq.campo.CampoCadeiaPrefixado(*args, **kwargs)**

    Base: `estrutarq.dado.dado_comum.DadoPrefixado
    <Estrutarq.Dado#estrutarq.dado.DadoPrefixado>`_,
    `estrutarq.campo.campo_cadeia.CampoCadeiaBasico
    <#estrutarq.campo.CampoCadeiaBasico>`_

    Classe para cadeia de caracteres prefixada pelo comprimento_bloco


Campo cadeia de comprimento fixo
--------------------------------

**class estrutarq.campo.CampoCadeiaFixo(comprimento: int, **kwargs)**

    Base: `estrutarq.dado.dado_comum.DadoFixo
    <Estrutarq.Dado#estrutarq.dado.DadoFixo>`_,
    `estrutarq.campo.campo_cadeia.CampoCadeiaBasico
    <#estrutarq.campo.CampoCadeiaBasico>`_

    Classe para cadeia de caracteres com comprimento_bloco fixo e
    preenchimento de dados inválidos


Módulo ``campo_inteiro``
========================

``estrutarq.campo.campo_inteiro``


Campo inteiro básico
--------------------

**class estrutarq.campo.campo_inteiro.CampoIntBasico(tipo: str, valor:
int = 0)**

    Base: `estrutarq.campo.campo_comum.CampoBasico
    <#estrutarq.campo.CampoBasico>`_

    Classe básica para campo inteiro

    **bytes_para_valor(dado: bytes)**

        Conversão de uma sequência de bytes (representação textual)
        para inteiro :param dado: sequência de bytes

    ``property valor:
    https://docs.python.org/3/library/functions.html#int``

        Recuperação, com as devidas conversões, do atributo
        ``__valor`` :return: o valor de ``__valor``

    **valor_para_bytes() ->
    https://docs.python.org/3/library/stdtypes.html#bytes**

        Conversão do valor inteiro para sequência de bytes usando
        representação textual e codificação UTF-8 :return: sequência
        de bytes


Campo inteiro com terminador
----------------------------

**class estrutarq.campo.CampoIntTerminador(terminador: bytes =
b'\x00', **kwargs)**

    Base: `estrutarq.dado.dado_comum.DadoTerminador
    <Estrutarq.Dado#estrutarq.dado.DadoTerminador>`_,
    `estrutarq.campo.campo_inteiro.CampoIntBasico
    <#estrutarq.campo.campo_inteiro.CampoIntBasico>`_

    Classe para inteiro textual com terminador


Campo inteiro prefixado pelo comprimento
----------------------------------------

**class estrutarq.campo.CampoIntPrefixado(**kwargs)**

    Base: `estrutarq.dado.dado_comum.DadoPrefixado
    <Estrutarq.Dado#estrutarq.dado.DadoPrefixado>`_,
    `estrutarq.campo.campo_inteiro.CampoIntBasico
    <#estrutarq.campo.campo_inteiro.CampoIntBasico>`_

    Classe para inteiro textual com prefixo de comprimento_bloco


Campo inteiro binário
---------------------

**class estrutarq.campo.CampoIntBinario(**kwargs)**

    Base: `estrutarq.dado.dado_comum.DadoBinario
    <Estrutarq.Dado#estrutarq.dado.DadoBinario>`_,
    `estrutarq.campo.campo_inteiro.CampoIntBasico
    <#estrutarq.campo.campo_inteiro.CampoIntBasico>`_

    Classe para inteiro em formato binário (big endian) com 8 bytes e
    complemento para 2 para valores negativos

    **bytes_para_valor(dado: bytes)**

        Conversão de uma sequência de bytes (binária big-endian com
        sinal) para inteiro :param dado: sequência de bytes

    ``numero_bytes = 8``

    **valor_para_bytes() ->
    https://docs.python.org/3/library/stdtypes.html#bytes**

        Conversão do valor inteiro para sequência de bytes usando
        representação binária big-endian com sinal :return: sequência
        de bytes


Campo inteiro de comprimento fixo
---------------------------------

**class estrutarq.campo.CampoIntFixo(comprimento: int, **kwargs)**

    Base: `estrutarq.dado.dado_comum.DadoFixo
    <Estrutarq.Dado#estrutarq.dado.DadoFixo>`_,
    `estrutarq.campo.campo_inteiro.CampoIntBasico
    <#estrutarq.campo.campo_inteiro.CampoIntBasico>`_

    Classe para inteiro textual com tamanho fixo


Módulo ``campo_real``
=====================

``estrutarq.campo.campo_real``


Campo real básico
-----------------

**class estrutarq.campo.campo_real.CampoRealBasico(tipo: str, valor:
float = 0)**

    Base: `estrutarq.campo.campo_comum.CampoBasico
    <#estrutarq.campo.CampoBasico>`_

    Classe básica para campo real

    **bytes_para_valor(dado: bytes)**

        Conversão de sequência de bytes com valor textual para valor
        real :param dado: sequência de 8 bytes

    ``property valor:
    https://docs.python.org/3/library/functions.html#float``

        Recuperação, com as devidas conversões, do atributo
        ``__valor`` :return: o valor de ``__valor``

    **valor_para_bytes() ->
    https://docs.python.org/3/library/stdtypes.html#bytes**

        Conversão do valor do campo para sequência de bytes textual
        :return: a sequência de bytes no padrão especificado


Campo real com terminador
-------------------------

**class estrutarq.campo.CampoRealTerminador(terminador: bytes =
b'\x00', **kwargs)**

    Base: `estrutarq.dado.dado_comum.DadoTerminador
    <Estrutarq.Dado#estrutarq.dado.DadoTerminador>`_,
    `estrutarq.campo.campo_real.CampoRealBasico
    <#estrutarq.campo.campo_real.CampoRealBasico>`_

    Classe para campo real com representação textual de
    comprimento_bloco fixo


Campo real prefixado pelo comprimento
-------------------------------------

**class estrutarq.campo.CampoRealPrefixado(**kwargs)**

    Base: `estrutarq.dado.dado_comum.DadoPrefixado
    <Estrutarq.Dado#estrutarq.dado.DadoPrefixado>`_,
    `estrutarq.campo.campo_real.CampoRealBasico
    <#estrutarq.campo.campo_real.CampoRealBasico>`_

    Classe para campo real com representação textual de
    comprimento_bloco fixo


Campo real binário
------------------

**class estrutarq.campo.CampoRealBinario(**kwargs)**

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

**class estrutarq.campo.CampoRealFixo(comprimento: int, **kwargs)**

    Base: `estrutarq.dado.dado_comum.DadoFixo
    <Estrutarq.Dado#estrutarq.dado.DadoFixo>`_,
    `estrutarq.campo.campo_real.CampoRealBasico
    <#estrutarq.campo.campo_real.CampoRealBasico>`_

    Classe para campo real com representação textual de
    comprimento_bloco fixo
