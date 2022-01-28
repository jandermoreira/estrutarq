#
#  Blocos
#

from dado import DadoFixo
from typing import BinaryIO

class Bloco(DadoFixo):
    def __init__(self, comprimento: int, arquivo: BinaryIO):
        self._arquivo = arquivo
        super.__init__()
