"""
Compressão pelo método de Huffman.

Base:
Huffman, D. A. "A method for the construction of minimum-redundancy codes".
Proceedings of the IRE, IEEE, 1952, 40, 1098-1101

..
    Licença: GNU GENERAL PUBLIC LICENSE V.3, 2007
    Jander Moreira, 2021, 2022
"""

from typing import Any

class Huffman:
    def __init__(self):
        pass


class NoArvoreBinaria:
    def __init__(self, valor: Any,
                 esquerda: NoArvoreBinaria = None,
                 direita: NoArvoreBinaria = None):
        """

        :param valor:
        """
        self.valor = valor
        self.esquerda = esquerda
        self.direita = direita
