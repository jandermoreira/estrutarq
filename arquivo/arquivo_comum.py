#
#  Arquivos
#

# from os import fstat
from abc import ABCMeta, abstractmethod
from os.path import exists
from estrutarq.registro import RegistroBasico


class ArquivoBasico(metaclass = ABCMeta):
    """
    Gerenciador dedicado a um único arquivo aberto
    """

    def __init__(self, nome_arquivo: str, tipo: str, novo: bool = False):
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
        Iniciação necessária depois da criação de um novo arquivo
        """
        pass

    @abstractmethod
    def _inicie_arquivo_existente(self):
        """
        Iniciação necessária depois da abertura de um arquivo já existente
        """
        pass

    @abstractmethod
    def leia(self) -> RegistroBasico:
        """
        Leitura de um registro do arquivo
        :return: o registro lido
        """
        pass

    @abstractmethod
    def escreva(self, registro: RegistroBasico):
        """
        Gravação de um registro no arquivo
        """
        pass

    def feche(self):
        """
        Fechamento do arquivo associado
        """
        self.arquivo.close()

    def __str__(self):
        """
        Descrição textual do arquivo
        """
        return f"Nome do arquivo: {self.nome_arquivo}"


class ArquivoSimplesFixo(ArquivoBasico):
    """
    Gerenciador de arquivo simples (como fluxo de dados) com registros de
    comprimento fixo.
    """

    def __init__(self, nome_arquivo: str, esquema_registro: RegistroBasico,
                 **kwargs):
        self.registro = esquema_registro
        self.comprimento_registro = registro._comprimento()
        print(self.comprimento_registro)
        super().__init__(nome_arquivo, "simples fixo", **kwargs)

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

    def leia(self) -> bytes:
        """
        Leitura dos dados do arquivo
        :return: a sequência de bytes lida
        """

    def escreva(self, registro: RegistroBasico, posicao_relativa: int = None):
        """
        Gravação de um registro no arquivo
        """
        if posicao_relativa != None:
            self.arquivo.seek(posicao_relativa * self.comprimento_registro)
        registro.escreva(self.arquivo)

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
