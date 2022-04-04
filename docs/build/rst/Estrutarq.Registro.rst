
Pacote ``estrutarq.registro``
*****************************


Módulo ``estrutarq.registro.registro_comum``
============================================

Registros

**class estrutarq.registro.registro_comum.RegistroBasico(tipo: str,
*lista_campos)**

    Base: `estrutarq.dado.dado_comum.DadoBasico
    <Estrutarq.Dado#estrutarq.dado.DadoBasico>`_

    Classe básica para registros

    **Utiliza @DynamicAttrs**

    **adicione_campos(*lista_campos)**

        Inclusão de uma sequência de campos ao registro :param
        lista_campos: uma sequência de um ou mais campos, cada um

            especificado pela tupla (nome_arquivo, campo), com
            nome_arquivo (str) sendo o nome_arquivo do campo e campo
            sendo uma instância de um campo válido

    **comprimento()**

        Retorna o comprimento do registro em bytes caso ele tenha
        comprimento total fixo :return: o comprimento do registro em
        bytes ou None se tiver comprimento variável

    **copy()**

        Cópia “profunda” deste campo :return: outra instância com os
        mesmos valores

    **de_bytes(dados_registro: bytes)**

        Obtenção dos bytes de cada campo a partir dos bytes do
        registro inteiro :param dados_registro: sequência de bytes do
        registro

    **escreva(arquivo)**

        Escrita do registro no arquivo :param arquivo:

    **leia(arquivo)**

        Obtenção de um registro a partir do arquivo :param arquivo:
        arquivo binário aberto com permissão de leitura

    **para_bytes() ->
    https://docs.python.org/3/library/stdtypes.html#bytes**

        Criação dos bytes do registro pela concatenação dos bytes dos
        campos, sucessivamente :return: sequência dos bytes dos campos

    **tem_comprimento_fixo()**

        Verifica se o registro tem comprimento fixo :return: True se o
        comprimento for fixo

        O registro é considerado de tamanho fixo se qualquer uma das
        propriedades foram verdadeiras:

            1.  o registro tem é marcado com _comprimento_fixo == True

            2.  todos os campos tiverem comprimento fixo

    ``property tipo``

**class
estrutarq.registro.registro_comum.RegistroBruto(*lista_campos)**

    Base: `estrutarq.dado.dado_comum.DadoBruto
    <Estrutarq.Dado#estrutarq.dado.DadoBruto>`_,
    `estrutarq.registro.registro_comum.RegistroBasico
    <#estrutarq.registro.registro_comum.RegistroBasico>`_

    Classe básica para registro, com controle exclusivamente pelo
    número de campos

    Utiliza @DynamicAttrs

**class estrutarq.registro.registro_comum.RegistroFixo(comprimento:
int, *lista_campos)**

    Base: `estrutarq.dado.dado_comum.DadoFixo
    <Estrutarq.Dado#estrutarq.dado.DadoFixo>`_,
    `estrutarq.registro.registro_comum.RegistroBasico
    <#estrutarq.registro.registro_comum.RegistroBasico>`_

    Classe para registros com terminador

**class
estrutarq.registro.registro_comum.RegistroPrefixado(*lista_campos)**

    Base: `estrutarq.dado.dado_comum.DadoPrefixado
    <Estrutarq.Dado#estrutarq.dado.DadoPrefixado>`_,
    `estrutarq.registro.registro_comum.RegistroBasico
    <#estrutarq.registro.registro_comum.RegistroBasico>`_

    Classe para registros prefixados pelo comprimento

**class
estrutarq.registro.registro_comum.RegistroTerminador(*lista_campos)**

    Base: `estrutarq.dado.dado_comum.DadoTerminador
    <Estrutarq.Dado#estrutarq.dado.DadoTerminador>`_,
    `estrutarq.registro.registro_comum.RegistroBasico
    <#estrutarq.registro.registro_comum.RegistroBasico>`_

    Classe para registros com terminador
