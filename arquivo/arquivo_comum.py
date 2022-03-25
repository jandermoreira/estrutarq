#
#  Arquivos
#

# from os import fstat
from abc import ABCMeta, abstractmethod
from os.path import exists


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
            Criação de um arquivo novo, com seu cabeçalho
        """
        try:
            self._arquivo = open(self.nome_arquivo, "wb")
        except IOError:
            raise IOError(f"Erro de criação do arquivo {self.nome_arquivo}.")
        else:
            self.inicie_arquivo_novo()

    def _abra_arquivo_existente(self):
        """

        """
        try:
            self._arquivo = open(self.nome_arquivo, "rb")
        except IOError:
            raise IOError(f"Erro de abertura do arquivo {self.nome_arquivo}.")
        else:
            self.inicie_arquivo_existente()

    @abstractmethod
    def inicie_arquivo_novo(self):
        """
        Iniciação necessária à criação de um novo arquivo
        """
        pass

    @abstractmethod
    def inicie_arquivo_existente(self):
        """
        Iniciação necessária para a abertura de um arquivo já existente
        """
        pass


class ArquivoSimplesFixo(ArquivoBasico):
    """
    Gerenciador de arquivo simples (como fluxo de dados) com registros de
    comprimento fixo.
    """

    def __init__(self, nome_arquivo: str, comprimento_registro: int):
        super().__init__(nome_arquivo, "simples fixo")
        self.comprimento_registro = comprimento_registro

    def inicie_arquivo_novo(self):
        pass

    def inicie_arquivo_existente(self):
        pass

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
