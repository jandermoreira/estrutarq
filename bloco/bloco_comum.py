#
#  Blocos
#

from typing import BinaryIO

from dado import DadoFixo


class Bloco(DadoFixo):
    def __init__(self, comprimento: int, arquivo: BinaryIO):
        self._arquivo = arquivo
        super.__init__()
