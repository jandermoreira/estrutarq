#
#  Blocos
#

from typing import BinaryIO
from os import fstat


# from dado import DadoFixo

class GerenciadorArquivo:
    """
    Gerenciador dedicado a um único arquivo aberto. O arquivo pode ser
    simples ou usando blocos, cada um deles podendo conter registros de
    comprimento fixo ou variável
    """

    def __init__(self, arquivo: BinaryIO, tipo: str):
        self.tipo = tipo
        self.arquivo = arquivo


class GASimplesFixo(GerenciadorArquivo):
    """
    Gerenciador de arquivo simples (como fluxo de dados) com registros de
    comprimento fixo.
    """

    def __init__(self, arquivo: BinaryIO, comprimento_registro: int):
        super().__init__(arquivo, "simples fixo")
        self.comprimento_registro = comprimento_registro


class GABloco:

    def __init__(self, arquivo: BinaryIO, comprimento_bloco: int):
        self.arquivo = arquivo
        self.comprimento_bloco = comprimento_bloco
        self.proximo_novo = fstat(
            self.arquivo.fileno()).st_size / comprimento_bloco


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
