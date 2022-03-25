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
        Iniciação necessária à criação de um novo arquivo
        """
        pass

    @abstractmethod
    def _inicie_arquivo_existente(self):
        """
        Iniciação necessária para a abertura de um arquivo já existente
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

    def __init__(self, nome_arquivo: str, comprimento_registro: int, **kwargs):
        super().__init__(nome_arquivo, "simples fixo", **kwargs)
        self.comprimento_registro = comprimento_registro

    def _inicie_arquivo_novo(self):
        pass

    def _inicie_arquivo_existente(self):
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
