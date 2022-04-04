
estrutarq.utilitarios package
*****************************


Submodules
==========


estrutarq.utilitarios.disco module
==================================

Rotinas utilitárias gerais

**estrutarq.utilitarios.disco.comprimento_de_bloco(diretorio:
Optional[str] = None)**

    Determina o comprimento_bloco de um bloco de disco, tendo como
    referência o disco onde está o diretório temporário do sistema;
    para outro disco, é preciso informar um diretório nesse disco em
    que haja direito de criação de arquivos. :param diretorio: um
    diretório no disco a ser verificado :return: o tamanho do bloco no
    disco

    Efeitos colaterais: é criado um arquivo temporário, que em seguida
    é removido.

**estrutarq.utilitarios.disco.main()**


estrutarq.utilitarios.dispositivo module
========================================

Rotinas utilitárias gerais

**estrutarq.utilitarios.dispositivo.comprimento_de_bloco(diretorio:
Optional[str] = None)**

    Determina o comprimento_bloco de um bloco do dispositivo externo,
    tendo como referência aquele onde está o diretório temporário do
    sistema (parãmetro igual a None); se um diretório em que haja
    direito de criação de arquivos for informado, então o dispostivo
    em que ele está será utilizado. :param diretorio: um diretório no
    disco a ser verificado :return: o tamanho do bloco no disco

    Efeitos colaterais: é criado um arquivo temporário, que em seguida
    é removido.

**estrutarq.utilitarios.dispositivo.main()**


estrutarq.utilitarios.geral module
==================================

Funções gerais

**estrutarq.utilitarios.geral.verifique_versao()**


estrutarq.utilitarios.interpretador module
==========================================


Module contents
===============
