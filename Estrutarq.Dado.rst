
Pacote ``estrutarq.dado``
*************************

Implementação de organizações de dados.


Módulo ``dado_comum``
=====================

``estrutarq.dado.dado_comum``

Estruturação de dados para armazenamento interno, gravação e leitura,
usando representações diversas:

    *   Em representação bruta

    *   Com terminador

    *   Prefixada pelo comprimento

    *   Em formato binário

    *   De comprimento fixo predefinido


Dado básico
-----------

Todas as demais classes do módulo são derivadas de uma classe abstrata
básica.

**class DadoBasico**

    Base: https://docs.python.org/3/library/functions.html#object

    Classe básica para armazenamento e manipulação de dados.

    Implementa as operações básicas e define os métodos abstratos.


Dado bruto
----------

**class DadoBruto**

    Base: `estrutarq.dado.dado_comum.DadoBasico
    <#estrutarq.dado.DadoBasico>`_

    Classe para dado em forma bruta, ou seja, sem acréscimo de
    qualquer forma de organização de dados.

    Campos brutos não possuem aplicação prática e são usados apenas
    para fins didáticos.


Dado com terminador
-------------------

**class DadoTerminador(terminador: bytes)**

    Base: `estrutarq.dado.dado_comum.DadoBasico
    <#estrutarq.dado.DadoBasico>`_

    Classe para implementação de dados com terminador. O dado é
    tratado como uma sequência de bytes à qual um byte predefinido
    (``terminador``) é acrescentado ao final para demarcar o fim dos
    dados. A existência do valor do byte terminador na sequência de
    dados é tratada com a técnica de enchimento de bytes (implementada
    em `DadoBasico <#estrutarq.dado.DadoBasico>`_).

    :Parâmetros:
        **terminador**
        (https://docs.python.org/3/library/stdtypes.html#bytes) – um
        byte a ser usado como terminador


Dado prefixado pelo comprimento
-------------------------------

**class DadoPrefixado**

    Base: `estrutarq.dado.dado_comum.DadoBasico
    <#estrutarq.dado.DadoBasico>`_

    Classe para a implementação de dado prefixado pelo seu
    comprimento. O prefixo é um valor inteiro binário de 2 bytes, sem
    sinal e com ordenação de bytes *big-endian*.


Dado binário
------------

**class DadoBinario(comprimento: int)**

    Base: `estrutarq.dado.dado_comum.DadoBasico
    <#estrutarq.dado.DadoBasico>`_

    Classe para a implementação de dado como sequência de bytes (i.e.,
    formato binário) com um determinado comprimento fixo em bytes.

    :Parâmetros:
        **comprimento**
        (https://docs.python.org/3/library/functions.html#int) –
        comprimento em bytes do valor a ser armazenado


Dado de comprimento fixo
------------------------

**class DadoFixo(comprimento: int, preenchimento: bytes = b'\xff')**

    Base: `estrutarq.dado.dado_comum.DadoBasico
    <#estrutarq.dado.DadoBasico>`_

    Classe para a implementação de dado de comprimento fixo em
    representação textual (i.e., sequência de caracteres). Caso o
    comprimento do dado seja inferior ao comprimento estabelecido para
    o campo, é feito o preenchimento dos bytes restantes com o valor
    `preenchimento <#estrutarq.dado.DadoFixo.preenchimento>`_. Caso o
    dado passado seja de comprimento superior ao definido, há o
    truncamento. Havendo a ocorrência do byte de preenchimento nos
    bytes de dados, é feito o enchimento de bytes. O preenchimento e o
    truncamento são feitos depois do enchimento.

    :Parâmetros:
        *   **comprimento**
            (https://docs.python.org/3/library/functions.html#int) – o
            comprimento em bytes fixado para o dado

        *   **preenchimento**
            (https://docs.python.org/3/library/stdtypes.html#bytes*,
            **opcional*) – um byte usado para preenchimento do espaço
            não usado para dado (valor padrão ``0xFF``)

    ``property preenchimento:
    https://docs.python.org/3/library/stdtypes.html#bytes``

        Um único byte usado para o preenchimento do espaço não usado
        dentro do comprimento final do campo. Valor padrão ``0xFF``.

    **leia_de_arquivo(arquivo: BinaryIO) ->
    https://docs.python.org/3/library/stdtypes.html#bytes**

        Leitura de um único dado de comprimento fixo a partir do
        arquivo, com remoção de bytes de enchimento e supressão do
        preenchimento.

        :Parâmetros:
            **arquivo** (*BinaryIO*) – arquivo binário aberto com
            permissão de leitura

        :Retorna:
            os bytes do dado, removidos o enchimento e preenchimento

        :Tipo de retorno:
            https://docs.python.org/3/library/stdtypes.html#bytes

        :Levanta:
            https://docs.python.org/3/library/exceptions.html#EOFError
            – se o arquivo não contiver a quantidade de bytes esperada
            definida pelo comprimento do dado

    **leia_de_bytes(sequencia: bytes) ->
    https://docs.python.org/3/library/stdtypes.html#tuple[https://docs.python.org/3/library/stdtypes.html#bytes,
    https://docs.python.org/3/library/stdtypes.html#bytes]**

        Recuperação de um dado individual de uma sequência de bytes,
        retornando o dado sem os bytes de preenchimento e o restante
        da sequência.

        :Parâmetros:
            **sequencia** – uma sequência de bytes

        :Retorna:
            tupla com os bytes do dado, removidos os bytes de
            enchimento e preenchimento, e a sequência de bytes
            restante

        :Tipo de retorno:
            https://docs.python.org/3/library/stdtypes.html#tuple[https://docs.python.org/3/library/stdtypes.html#bytes,
            https://docs.python.org/3/library/stdtypes.html#bytes]

        :Levanta:
            https://docs.python.org/3/library/exceptions.html#TypeError
            – se o comprimento da sequência tem menos bytes que o
            definido para o comprimento do campo

    **adicione_formatacao(dado: bytes) ->
    https://docs.python.org/3/library/stdtypes.html#bytes**

        Formatação do dado: ajusta o dado para o comprimento definido,
        com uso de enchimento de bytes para as ocorrências do byte de
        preenchimento, seguido do truncamento ou acréscimo o byte de
        preenchimento.

        :Parâmetros:
            **dado**
            (https://docs.python.org/3/library/stdtypes.html#bytes) –
            valor do dado

        :Retorna:
            o dado enchido e formatado no comprimento especificado

        :Tipo de retorno:
            https://docs.python.org/3/library/stdtypes.html#bytes

        :Levanta:
            https://docs.python.org/3/library/exceptions.html#ValueError
            – se a operação de truncamento causar corrupção no dado
            armazenado (e.g., o truncamento ocorrer entre o byte de
            enchimento e o próximo byte)

    **remova_formatacao(sequencia: bytes) ->
    https://docs.python.org/3/library/stdtypes.html#bytes**

        Desformatação do dado: remoção do enchimento e de eventuais
        bytes de preenchimento.

        :Parâmetros:
            **sequencia**
            (https://docs.python.org/3/library/stdtypes.html#bytes) –
            bytes de dados

        :Retorna:
            dado efetivo, sem enchimento ou preenchimento

        :Tipo de retorno:
            https://docs.python.org/3/library/stdtypes.html#bytes

        :Levanta:
            https://docs.python.org/3/library/exceptions.html#TypeError
            – se o comprimento da sequência de bytes diferir do
            comprimento especificado para o dado
