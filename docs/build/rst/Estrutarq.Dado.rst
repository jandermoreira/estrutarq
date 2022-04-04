
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

Licença: GNU GENERAL PUBLIC LICENSE V.3, 2007

Jander Moreira, 2022


Dado básico
-----------

Todas as demais classes do módulo são derivadas de uma classe abstrata
básica.

**class estrutarq.dado.DadoBasico**

    Base: https://docs.python.org/3/library/functions.html#object

    Classe básica para armazenamento e manipulação de dados.

    Implementa as operações básicas e define os métodos abstratos.

    **abstract adicione_formatacao(dado: bytes) ->
    https://docs.python.org/3/library/stdtypes.html#bytes**

        Acréscimo da organização de dados em uso aos bytes do dado.

        :Parâmetros:
            **dado**
            (https://docs.python.org/3/library/stdtypes.html#bytes) –
            bytes do dado

        :Retorna:
            bytes do dado acrescido da forma de organização

        :Tipo de retorno:
            https://docs.python.org/3/library/stdtypes.html#bytes

    ``byte_enchimento:
    https://docs.python.org/3/library/stdtypes.html#bytes = b'\x1b'``

        Contém o byte de escape usado para enchimento (*byte
        stuffing*). Valor padrão: ``ESC`` (hexadecimal ``0x1B``).

    **enchimento_de_bytes(sequencia: bytes, lista_bytes: list[bytes])
    -> https://docs.python.org/3/library/stdtypes.html#bytes**

        Operação de enchimento de bytes (*byte stuffing*). Antes de
        cada item de ``lista_bytes`` é acrescentado o byte
        ``byte_enchimento``.

        :Parâmetros:
            *   **sequencia**
                (https://docs.python.org/3/library/stdtypes.html#bytes)
                – a sequência de bytes a ser “enchida”

            *   **lista_bytes**
                (https://docs.python.org/3/library/stdtypes.html#list*[*https://docs.python.org/3/library/stdtypes.html#bytes*]*)
                – os bytes especiais que serão “escapados”

        :Retorna:
            a sequência original enchida

        :Tipo de retorno:
            https://docs.python.org/3/library/stdtypes.html#bytes

    **esvaziamento_de_bytes(sequencia: bytes) ->
    https://docs.python.org/3/library/stdtypes.html#bytes**

        Operação de esvaziamento de bytes (*byte un-stuffing*). Todos
        os enchimentos feitos com ``byte_enchimento`` são removidos.

        :Parâmetros:
            **sequencia**
            (https://docs.python.org/3/library/stdtypes.html#bytes) –
            a sequência de bytes a ser “esvaziada”

        :Retorna:
            a sequência sem os enchimentos

        :Tipo de retorno:
            https://docs.python.org/3/library/stdtypes.html#bytes

    **abstract leia_de_arquivo(arquivo: BinaryIO) ->
    https://docs.python.org/3/library/stdtypes.html#bytes**

        Recuperação de um dado lido de um arquivo, observando a
        representação do dado e a forma de organização. A forma de
        organização usada é removida.

        :Parâmetros:
            **arquivo** (*BinaryIO*) – arquivo binário aberto com
            permissão de leitura

        :Retorna:
            a sequência de bytes lida

        :Tipo de retorno:
            https://docs.python.org/3/library/stdtypes.html#bytes

    **abstract leia_de_bytes(sequencia: bytes) ->
    https://docs.python.org/3/library/stdtypes.html#tuple[https://docs.python.org/3/library/stdtypes.html#bytes,
    https://docs.python.org/3/library/stdtypes.html#bytes]**

        Recuperação de um dado a partir de uma sequência de bytes,
        retornando os bytes do dado em si e o restante da sequência
        depois da extração do dado, observando a representação do dado
        e a forma de organização. O dado é retornado sem a
        organização.

        :Parâmetros:
            **sequencia**
            (https://docs.python.org/3/library/stdtypes.html#bytes) –
            sequência de bytes

        :Retorna:
            tupla com os bytes do dado, removidos os bytes de
            organização de dados, e a sequência de bytes restante

        :Tipo de retorno:
            https://docs.python.org/3/library/stdtypes.html#tuple[https://docs.python.org/3/library/stdtypes.html#bytes,
            https://docs.python.org/3/library/stdtypes.html#bytes]

    **abstract remova_formatacao(sequencia: bytes) ->
    https://docs.python.org/3/library/stdtypes.html#bytes**

        Remoção dos bytes correspondentes à forma de organização da
        sequência de bytes.

        :Parâmetros:
            **sequencia**
            (https://docs.python.org/3/library/stdtypes.html#bytes) –
            uma sequência de bytes

        :Retorna:
            a sequência após extraídos os bytes de organização

        :Tipo de retorno:
            https://docs.python.org/3/library/stdtypes.html#bytes

    **varredura_com_enchimento(sequencia: bytes, referencia: bytes) ->
    https://docs.python.org/3/library/stdtypes.html#tuple[https://docs.python.org/3/library/stdtypes.html#bytes,
    https://docs.python.org/3/library/stdtypes.html#bytes]**

        Recuperação de um dado individual de uma sequência de bytes,
        retornando o dado até um byte de referência (não “enchido”) e
        o restante da sequência depois desse byte.

        :Parâmetros:
            *   **sequencia**
                (https://docs.python.org/3/library/stdtypes.html#bytes)
                – uma sequência de bytes

            *   **referencia**
                (https://docs.python.org/3/library/stdtypes.html#bytes)
                – byte simples usado como sentinela (terminador)

        :Retorna:
            uma tupla contendo a sequência de bytes até ``referencia``
            e o restante da sequência depois de ``referencia``

        :Tipo de retorno:
            https://docs.python.org/3/library/stdtypes.html#tuple[https://docs.python.org/3/library/stdtypes.html#bytes,
            https://docs.python.org/3/library/stdtypes.html#bytes]

        :Levanta:
            https://docs.python.org/3/library/exceptions.html#ValueError
            – se o byte de referência não estiver presente na
            sequência de bytes


Dado bruto
----------

**class estrutarq.dado.DadoBruto**

    Base: `estrutarq.dado.dado_comum.DadoBasico
    <#estrutarq.dado.DadoBasico>`_

    Classe para dado em forma bruta, ou seja, sem acréscimo de
    qualquer forma de organização de dados.

    Campos brutos não possuem aplicação prática e são usados apenas
    para fins didáticos.

    **adicione_formatacao(dado: bytes) ->
    https://docs.python.org/3/library/stdtypes.html#bytes**

        Para dado bruto não há acréscimo de bytes de organização de
        dados e o dado é repassado sem modificação.

        :Parâmetros:
            **dado**
            (https://docs.python.org/3/library/stdtypes.html#bytes) –
            bytes do dado

        :Retorna:
            bytes do dado inalterados

        :Tipo de retorno:
            https://docs.python.org/3/library/stdtypes.html#bytes

    **leia_de_arquivo(arquivo: BinaryIO)**

        Recuperação de um dado lido de um arquivo (inviável para dado
        bruto).

        :Parâmetros:
            **arquivo** (*BinaryIO*) – arquivo binário aberto com
            permissão de leitura

        :Levanta:
            **NotImplemented** – se o método for acidentalmente
            chamado

    **leia_de_bytes(sequencia: bytes)**

        Recuperação de um dado extraído de uma sequência de bytes
        (inviável para dado bruto).

        :Parâmetros:
            **sequencia**
            (https://docs.python.org/3/library/stdtypes.html#bytes) –
            sequência de bytes

        :Levanta:
            **NotImplemented** – se o método for acidentalmente
            chamado

    **remova_formatacao(sequencia: bytes) ->
    https://docs.python.org/3/library/stdtypes.html#bytes**

        Para o dado bruto não há bytes de organização a sequência de
        bytes é repassada sem modificação.

        :Parâmetros:
            **sequencia**
            (https://docs.python.org/3/library/stdtypes.html#bytes) –
            uma sequência de bytes

        :Retorna:
            a sequência inalterada

        :Tipo de retorno:
            https://docs.python.org/3/library/stdtypes.html#bytes


Dado com terminador
-------------------

**class estrutarq.dado.DadoTerminador(terminador: bytes)**

    Base: `estrutarq.dado.dado_comum.DadoBasico
    <#estrutarq.dado.DadoBasico>`_

    Classe para implementação de dados com terminador. O dado é
    tratado como uma sequência de bytes à qual um byte predefinido
    (`terminador <#estrutarq.dado.DadoTerminador.terminador>`_) é
    acrescentado ao final para demarcar o fim dos dados. A existência
    do valor do byte terminador na sequência de dados é tratada com a
    técnica de enchimento de bytes (implementada em `DadoBasico
    <#estrutarq.dado.DadoBasico>`_).

    :Parâmetros:
        **terminador**
        (https://docs.python.org/3/library/stdtypes.html#bytes) – um
        byte a ser usado como terminador

    **adicione_formatacao(dado: bytes) ->
    https://docs.python.org/3/library/stdtypes.html#bytes**

        Formatação do dado: uso de ‘byte stuffing’ para permitir o
        byte terminador como dado e acréscimo do byte terminador.

        :Parâmetros:
            **dado**
            (https://docs.python.org/3/library/stdtypes.html#bytes) –
            sequência de bytes do dado

        :Retorna:
            a sequência de dados enchida e com o acréscimo do
            terminador ao final

        :Tipo de retorno:
            https://docs.python.org/3/library/stdtypes.html#bytes

    **leia_de_arquivo(arquivo: BinaryIO) ->
    https://docs.python.org/3/library/stdtypes.html#bytes**

        Leitura de um único dado com terminador. A leitura é feita
        byte a byte até que o byte terminador seja encontrado. Bytes
        terminadores enchidos são restaurados, mas não determinam o
        fim da busca. O enchimento de bytes é removido.

        :Parâmetros:
            **arquivo** – arquivo binário aberto com permissão de
            leitura

        :Retorna:
            a sequência de bytes do dado sem o terminador

        :Levanta:
            https://docs.python.org/3/library/exceptions.html#EOFError
            – se o fim do arquivo for atingido antes de o byte
            terminador ser encontrado

    **leia_de_bytes(sequencia: bytes) ->
    https://docs.python.org/3/library/stdtypes.html#tuple[https://docs.python.org/3/library/stdtypes.html#bytes,
    https://docs.python.org/3/library/stdtypes.html#bytes]**

        Recuperação de um dado individual de uma sequência de bytes,
        retornando o dado até o terminador e o restante da sequência
        depois do terminador.

        :Parâmetros:
            **sequencia**
            (https://docs.python.org/3/library/stdtypes.html#bytes) –
            uma sequência de bytes

        :Retorna:
            uma tupla contendo os bytes dos dados e a sequência de
            bytes restante, excluindo-se de ambas o terminador

        :Tipo de retorno:
            https://docs.python.org/3/library/stdtypes.html#tuple[https://docs.python.org/3/library/stdtypes.html#bytes,
            https://docs.python.org/3/library/stdtypes.html#bytes]

    **remova_formatacao(sequencia: bytes) ->
    https://docs.python.org/3/library/stdtypes.html#bytes**

        Desformatação do dado: remoção dos bytes de enchimento e
        também do byte terminador.

        :Parâmetros:
            **sequencia** – sequência de bytes de dados

        :Retorna:
            sequência de bytes de dados, esvaziada e sem terminador

        :Tipo de retorno:
            https://docs.python.org/3/library/stdtypes.html#bytes

        :Levanta:
            https://docs.python.org/3/library/exceptions.html#TypeError
            – se o terminador não estiver presente na sequência
            esvaziada

    ``property terminador:
    https://docs.python.org/3/library/stdtypes.html#bytes``

        Byte simples usado como terminador.


Dado prefixado pelo comprimento
-------------------------------

**class estrutarq.dado.DadoPrefixado**

    Base: `estrutarq.dado.dado_comum.DadoBasico
    <#estrutarq.dado.DadoBasico>`_

    Classe para a implementação de dado prefixado pelo seu
    comprimento. O prefixo é um valor inteiro binário de 2 bytes, sem
    sinal e com ordenação de bytes *big-endian*.

    **adicione_formatacao(dado: bytes) ->
    https://docs.python.org/3/library/stdtypes.html#bytes**

        Formatação do dado: acréscimo do prefixo binário com
        comprimento (2 bytes, *big-endian*, sem sinal).

        :Parâmetros:
            **dado**
            (https://docs.python.org/3/library/stdtypes.html#bytes) –
            sequência de bytes do dado

        :Retorna:
            a sequência de bytes prefixada por dois bytes com o
            comprimento

        :Tipo de retorno:
            https://docs.python.org/3/library/stdtypes.html#bytes

    **leia_de_arquivo(arquivo: BinaryIO) ->
    https://docs.python.org/3/library/stdtypes.html#bytes**

        Leitura de um único dado prefixado pelo comprimento a partir
        de um arquivo binário aberto. Os bytes de comprimento são
        removidos.

        :Parâmetros:
            **arquivo** (*BinaryIO*) – arquivo binário aberto com
            permissão de leitura

        :Retorna:
            sequência com os bytes do dado, sem o prefixo

        :Tipo de retorno:
            https://docs.python.org/3/library/stdtypes.html#bytes

        :Levanta:
            https://docs.python.org/3/library/exceptions.html#EOFError
            – se houver tentativa de leitura além do fim do arquivo

    **leia_de_bytes(sequencia: bytes) ->
    https://docs.python.org/3/library/stdtypes.html#tuple[https://docs.python.org/3/library/stdtypes.html#bytes,
    https://docs.python.org/3/library/stdtypes.html#bytes]**

        Recuperação de um dado individual de uma sequência de bytes,
        retornando o dado sem o prefixo e o restante da sequência.

        :Parâmetros:
            **sequencia**
            (https://docs.python.org/3/library/stdtypes.html#bytes) –
            uma sequência de bytes

        :Retorna:
            uma tupla com a sequência de bytes de dados sem o prefixo
            e o restante da sequência de entrada

        :Tipo de retorno:
            https://docs.python.org/3/library/stdtypes.html#tuple[https://docs.python.org/3/library/stdtypes.html#bytes,
            https://docs.python.org/3/library/stdtypes.html#bytes]

        :Levanta:
            https://docs.python.org/3/library/exceptions.html#TypeError
            – se a sequência contiver menos bytes que o necessário

    **remova_formatacao(sequencia: bytes) ->
    https://docs.python.org/3/library/stdtypes.html#bytes**

        Desformatação do dado: remoção dos dois bytes do comprimento.

        :Parâmetros:
            **sequencia**
            (https://docs.python.org/3/library/stdtypes.html#bytes) –
            bytes de dados

        :Retorna:
            dado efetivo, sem o prefixo de comprimento

        :Tipo de retorno:
            https://docs.python.org/3/library/stdtypes.html#bytes

        :Levanta:
            https://docs.python.org/3/library/exceptions.html#TypeError
            – se a sequência de bytes passada contém quantidade de
            bytes diferente do comprimento especificado


Dado binário
------------

**class estrutarq.dado.DadoBinario(comprimento: int)**

    Base: `estrutarq.dado.dado_comum.DadoBasico
    <#estrutarq.dado.DadoBasico>`_

    Classe para a implementação de dado como sequência de bytes (i.e.,
    formato binário) com um determinado comprimento fixo em bytes.

    :Parâmetros:
        **comprimento**
        (https://docs.python.org/3/library/functions.html#int) –
        comprimento em bytes do valor a ser armazenado

    **adicione_formatacao(dado: bytes) ->
    https://docs.python.org/3/library/stdtypes.html#bytes**

        Formatação do dado: apenas repassa o dado binário.

        :Parâmetros:
            **dado**
            (https://docs.python.org/3/library/stdtypes.html#bytes) –
            valor binário

        :Retorna:
            o dado sem modificação

        :Tipo de retorno:
            https://docs.python.org/3/library/stdtypes.html#bytes

        :Levanta:
            https://docs.python.org/3/library/exceptions.html#TypeError
            – se o comprimento do dado diferir do esperado

    **leia_de_arquivo(arquivo: BinaryIO) ->
    https://docs.python.org/3/library/stdtypes.html#bytes**

        Recuperação dos bytes do valor binário a partir de um arquivo
        dada a quantidade de bytes esperada.

        :Parâmetros:
            **arquivo** (*BinaryIO*) – arquivo binário aberto com
            permissão de leitura

        :Retorna:
            a sequência de bytes lidos

        :Tipo de retorno:
            https://docs.python.org/3/library/stdtypes.html#bytes

        :Levanta:
            https://docs.python.org/3/library/exceptions.html#EOFError
            – se o arquivo contiver menos bytes que a quantidade
            esperada

    **leia_de_bytes(sequencia: bytes) ->
    https://docs.python.org/3/library/stdtypes.html#tuple[https://docs.python.org/3/library/stdtypes.html#bytes,
    https://docs.python.org/3/library/stdtypes.html#bytes]**

        Recuperação de um dado binário de comprimento definido a
        partir de uma sequência de bytes.

        :Parâmetros:
            **sequencia**
            (https://docs.python.org/3/library/stdtypes.html#bytes) –
            sequência de bytes

        :Retorna:
            tupla com os bytes do dado no comprimento esperado e a
            sequência de bytes restante

        :Tipo de retorno:
            https://docs.python.org/3/library/stdtypes.html#tuple[https://docs.python.org/3/library/stdtypes.html#bytes,
            https://docs.python.org/3/library/stdtypes.html#bytes]

        :Levanta:
            https://docs.python.org/3/library/exceptions.html#TypeError
            – se a sequência contiver menos bytes que o esperado

    **remova_formatacao(sequencia: bytes) ->
    https://docs.python.org/3/library/stdtypes.html#bytes**

        Desformatação do dado: apenas repassa o dado binário.

        :Parâmetros:
            **sequencia**
            (https://docs.python.org/3/library/stdtypes.html#bytes) –
            sequência de bytes do valor binário

        :Retorna:
            a sequência sem modificação

        :Tipo de retorno:
            https://docs.python.org/3/library/stdtypes.html#bytes

        :Levanta:
            https://docs.python.org/3/library/exceptions.html#TypeError
            – se o comprimento do dado diferir do esperado


Dado de comprimento fixo
------------------------

**class estrutarq.dado.DadoFixo(comprimento: int, preenchimento: bytes
= b'\xff')**

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

    ``property preenchimento:
    https://docs.python.org/3/library/stdtypes.html#bytes``

        Um único byte usado para o preenchimento do espaço não usado
        dentro do comprimento final do campo. Valor padrão ``0xFF``.

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
