
estrutarq.arquivo package
*************************


Submodules
==========


estrutarq.arquivo.arquivo_comum module
======================================

**class estrutarq.arquivo.arquivo_comum.ArquivoBasico(nome_arquivo:
str, tipo: str, novo: bool = False)**

    Base: https://docs.python.org/3/library/functions.html#object

    Gerenciador dedicado a um único arquivo aberto

    **abstract escreva(registro:
    estrutarq.registro.registro_comum.RegistroBasico)**

        Gravação de um registro no arquivo

    **feche()**

        Fechamento do arquivo associado

    **abstract leia() ->
    `estrutarq.registro.registro_comum.RegistroBasico
    <Estrutarq.Registro#estrutarq.registro.registro_comum.RegistroBasico>`_**

        Leitura de um registro do arquivo :return: o registro lido

    **posicao_atual()**

        Posição atual do arquivo :return:

**class estrutarq.arquivo.arquivo_comum.ArquivoSimples(nome_arquivo:
str, esquema_registro:
estrutarq.registro.registro_comum.RegistroBasico, **kwargs)**

    Base: `estrutarq.arquivo.arquivo_comum.ArquivoBasico
    <#estrutarq.arquivo.arquivo_comum.ArquivoBasico>`_

    Gerenciador de arquivo simples (como fluxo de dados) com registros
    de comprimento fixo.

    **escreva(registro:
    estrutarq.registro.registro_comum.RegistroBasico, **kwargs)**

        Gravação de um registro no arquivo

        self.escreva_efetivo chama escreva_fixo ou escreva_variável,
        conforme o registro tenha comprimento fixo ou variável

    **escreva_fixo(registro:
    estrutarq.registro.registro_comum.RegistroBasico,
    posicao_relativa: Optional[int] = None)**

        Gravação de um registro no arquivo :param registro: o registro
        a ser escrito :param posicao_relativa: posição relativa do
        registro no arquivo,

            com o primeiro registro sendo o registro 0

    **escreva_variavel(registro:
    estrutarq.registro.registro_comum.RegistroBasico, deslocamento:
    Optional[int] = None)**

        Gravação de um registro no arquivo :param registro: o registro
        a ser escrito :param deslocamento: posição absoluta (byte
        offset) da posição

            de escrita

    **leia(**kwargs) ->
    `estrutarq.registro.registro_comum.RegistroBasico
    <Estrutarq.Registro#estrutarq.registro.registro_comum.RegistroBasico>`_**

        Leitura de um registro do arquivo :return: o registro lido

        self.leia_efetivo chama leia_fixo ou leia_variável, conforme o
        registro tenha comprimento fixo ou variável

    **leia_fixo(posicao_relativa: Optional[int] = None) ->
    `estrutarq.registro.registro_comum.RegistroBasico
    <Estrutarq.Registro#estrutarq.registro.registro_comum.RegistroBasico>`_**

        Leitura de um registro de comprimento fixo :param
        posicao_relativa: posição relativa do registro no arquivo,

            com o primeiro registro sendo o registro 0

        :Retorna:
            o registro lido

    **leia_variavel(posicao_relativa: Optional[int] = None) ->
    `estrutarq.registro.registro_comum.RegistroBasico
    <Estrutarq.Registro#estrutarq.registro.registro_comum.RegistroBasico>`_**

        Leitura de um registro de comprimento variavel :param
        posicao_relativa: posição relativa do registro no arquivo,

            com o primeiro registro sendo o registro 0

        :Retorna:
            o registro lido

        A determinação da posição relativa é feita por busca
        sequencial


Module contents
===============
