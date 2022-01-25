#
#  Blocos
#

from utilitarios.dispositivo import comprimento_de_bloco
import os


class Bloco:
    def __init__(self, arquivo):
        self._arquivo = arquivo
        self.comprimento_do_bloco = comprimento_de_bloco(
            os.path.dirname(arquivo.name))
