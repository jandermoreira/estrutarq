"""
Arquivos para o armazenamento de registros.

Uma classe básica :class:`~.estrutarq.arquivo.arquivo_comum.ArquivoBasico`
define uma classe abstrata (ABC) com as propriedades e métodos gerais. Dela
são derivados arquivos:

* Simples (sem considerar blocos*)
* Estruturados (considerando o blocos*)

* O termo *blocos* é usado no contexto do acesso aos dispositivos de
arqmazenamento em memória secundária.

..
    Licença: GNU GENERAL PUBLIC LICENSE V.3, 2007
    Jander Moreira, 2021, 2022
"""

from abc import ABCMeta, abstractmethod
from os.path import exists

from estrutarq.registro import RegistroBasico


class ArquivoBasico(metaclass = ABCMeta):
    """
    Classe básica para um gerenciador de dedicado a um único arquivo.

    Se o arquivo não existir, ele é criado. Se já existir, ele é aberto para
    acesso.

    :param str tipo: nome do tipo (passado pela subclasse)
    :param str nome_arquivo: nome do arquivo binário
    :param bool, opcional novo: se `True`, o arquivo é tornado vazio, mesmo
        que já preexistente (valor padrão: `False`)
    """

    def __init__(self, tipo: str, nome_arquivo: str, novo: bool = False):
        self.tipo = tipo
        self.nome_arquivo = nome_arquivo
        if not exists(self.nome_arquivo) or novo:
            self._crie_arquivo_novo()
        else:
            self._abra_arquivo_existente()

    def _crie_arquivo_novo(self):
        """
        Criação de um arquivo binário novo com permissão para leitura
        e escrita
        """
        try:
            self.arquivo = open(self.nome_arquivo, "wb+")
        except IOError as erro:
            raise IOError(f"Erro de crição do arquivo. {erro}")
        else:
            self._inicie_arquivo_novo()

    def _abra_arquivo_existente(self):
        """
        Abertura de um arquivo binário existente com permissão para leitura
        e escrita
        """
        try:
            self.arquivo = open(self.nome_arquivo, "rb+")
        except IOError as erro:
            raise IOError(f"Erro de abertura do arquivo. {erro}")
        else:
            self._inicie_arquivo_existente()

    @abstractmethod
    def _inicie_arquivo_novo(self):
        """
        Iniciação necessária depois da criação de um novo arquivo.
        """
        pass

    @abstractmethod
    def _inicie_arquivo_existente(self):
        """
        Iniciação necessária depois da abertura de um arquivo já existente.
        """
        pass

    @abstractmethod
    def leia(self) -> RegistroBasico:
        """
        Leitura de um registro do arquivo a partir da posição corrente. Ao
        final da leitura, a posição corrente é o próximo byte depois do último
        escrito.

        :return: o registro lido
        :rtype: RegistroBasico
        """
        pass

    @abstractmethod
    def escreva(self, registro: RegistroBasico):
        """
        Gravação de um registro no arquivo.

        :param RegistroBasico registro: um registro para ser gravado
        """
        pass

    def feche(self):
        """
        Fechamento do arquivo associado.
        """
        self.arquivo.close()

    def reabra(self):
        """
        O arquivo associado é aberto novamente, preservando o conteúdo.

        :raise FileNotFoundError: se o arquivo não existir
        """
        if exists(self.nome_arquivo):
            self._abra_arquivo_existente()
        else:
            raise FileNotFoundError(f"Arquivo não encontrado: " +
                                    f"{self.nome_arquivo}.")

    def posicao_atual(self):
        """
        Posição atual do arquivo.

        :return:
        """
        return self.arquivo.tell()

    def __str__(self) -> str:
        """
        Descrição textual do arquivo.
        """
        return f"Nome do arquivo: {self.nome_arquivo}"


class ArquivoSimples(ArquivoBasico):
    """
    Gerenciador de arquivo simples (como fluxo de dados) com registros de
    comprimento fixo ou variável. Nenhuma consideração sobre blocos ou
    outro aspecto de acesso ao dispositivo de armazenamento secundário é feita.
    """

    def __init__(self, nome_arquivo: str, esquema_registro: RegistroBasico,
                 **kwargs):
        ArquivoBasico.__init__(self, "simples", nome_arquivo, **kwargs)
        self.esquema_registro = esquema_registro.copia()
        if esquema_registro.tem_comprimento_fixo():
            self.comprimento_registro = esquema_registro.comprimento()
            self.leia_efetivo = self.leia_fixo
            self.escreva_efetivo = self.escreva_fixo
        else:
            self.leia_efetivo = self.leia_variavel
            self.escreva_efetivo = self.escreva_variavel

    def _inicie_arquivo_novo(self):
        """
        Iniciação necessária depois da criação de um novo arquivo
        """
        pass

    def _inicie_arquivo_existente(self):
        """
        Iniciação necessária depois da abertura de um arquivo já existente
        """
        pass

    def leia_fixo(self, posicao_relativa: int = None) -> RegistroBasico:
        """
        Leitura de um registro de comprimento, usando a posição corrente do
        arquivo. Ao final da escrita, a posição corrente é o próximo byte
        depois do último escrito.

        :param posicao_relativa: posição relativa do registro no arquivo,
            com o primeiro registro sendo o registro 0
        :return: o registro lido
        """
        registro = self.esquema_registro.copia()
        if posicao_relativa is not None:
            # posicionamento por acesso direto
            self.arquivo.seek(posicao_relativa * self.comprimento_registro)
        registro.leia(self.arquivo)
        return registro

    def escreva_fixo(self, registro: RegistroBasico,
                     posicao_relativa: int = None):
        """
        Gravação de um registro de comprimento fixo no arquivo. A gravação é
        feita a partir da posição corrente, a menos que especificada outra
        posição. As posições são relativas aos registros (e não ao deslocamento
        de bytes), sendo que o primeiro registro o de posição 0, o segundo de
        posição 1 e assim sucessivamente.

        Ao final, a posição corrente é a do próximo byte depois do último byte
        lido.

        :param registro: o registro a ser escrito
        :param posicao_relativa: posição relativa do registro no arquivo,
            com o primeiro registro sendo o registro 0
        """
        if posicao_relativa is not None:
            self.arquivo.seek(posicao_relativa * self.comprimento_registro)
        registro.escreva(self.arquivo)

    def leia_variavel(self, posicao_relativa: int = None) -> RegistroBasico:
        """
        Leitura de um registro de comprimento variavel. A leitura é feita a
        partir da posição corrente, a menos que seja especificada outra posição.
        As posições são relativas aos registros (e não ao deslocamento
        de bytes), sendo que o primeiro registro o de posição 0, o segundo de
        posição 1 e assim sucessivamente. Neste caso, a 

        Ao final, a posição corrente é a do próximo byte depois do último byte
        lido.

        A determinação da posição relativa é feita por busca sequencial

        :param posicao_relativa: posição relativa do registro no arquivo,
            com o primeiro registro sendo o registro 0
        :return: o registro lido
        """
        registro = self.esquema_registro.copia()
        if posicao_relativa is not None:
            # busca sequencial a partir do início do arquivo
            self.arquivo.seek(0)
            for i in range(posicao_relativa + 1):
                registro.leia(self.arquivo)
        else:
            # leitura do próximo
            registro.leia(self.arquivo)
        return registro

    def escreva_variavel(self, registro: RegistroBasico,
                         deslocamento: int = None):
        """
        Gravação de um registro no arquivo
        :param registro: o registro a ser escrito
        :param deslocamento: posição absoluta (byte offset) da posição
            de escrita
        """
        if deslocamento is not None:
            self.arquivo.seek(deslocamento)
        registro.escreva(self.arquivo)

    def leia(self, **kwargs) -> RegistroBasico:
        """
        Leitura de um registro do arquivo
        :return: o registro lido

        self.leia_efetivo chama leia_fixo ou leia_variável, conforme
        o registro tenha comprimento fixo ou variável
        """
        return self.leia_efetivo(**kwargs)

    def escreva(self, registro: RegistroBasico, **kwargs):
        """
        Gravação de um registro no arquivo

        self.escreva_efetivo chama escreva_fixo ou escreva_variável, conforme
        o registro tenha comprimento fixo ou variável
        """
        self.escreva_efetivo(registro, **kwargs)

# class GABloco:
#
#     def __init__(self, arquivo: BinaryIO, comprimento_bloco: int):
#         self.arquivo = arquivo
#         self.comprimento_bloco = comprimento_bloco
#         self.proximo_novo = fstat(
#             self.arquivo.fileno()).st_size / comprimento_bloco

# class BlocoBasico:
#     def __init__(self, comprimento_bloco: int):
#         self.comprimento = comprimento_bloco
#
#     def novo_bloco(self):
#         """
#         Criação de um novo bloco em MP
#         :return:
#         """
#
#
# class BlocoRegistrosFixos(BlocoBasico):
#     """
#     Blocos com registros de comprimento_bloco fixo:
#         -uso do byte offset para indicar o início de cada registro
#         -controle do espaço livre pelo número de bytes disponível
#     """
#
#     def __init__(self, comprimento_bloco: int, arquivo: BinaryIO,
#                  comprimento_registro: int):
#         super().__init__(comprimento_bloco)
#         self.comprimento_registro = comprimento_registro
