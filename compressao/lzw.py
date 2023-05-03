"""
Compressão pelo método LZW.

Código baseado no pseudocódigo apresentado em:
Drozdek, A. "Estrutura de dados e algoritmos em C++".
Cengage Learning, 2016

..
    Licença: GNU GENERAL PUBLIC LICENSE V.3, 2007
    Jander Moreira, 2021, 2022
"""

# todo: considerar https://stackoverflow.com/questions/4730993/python-key-in-dict-keys-performance-for-large-dictionaries

from typing import Union

from bitarray import bitarray
from bitarray.util import ba2int

from estrutarq.utilitarios.fluxo import Fluxo

comprimento_maximo_codigo = 12  # em bits


class LZWcompressor:
    """
    Classe para compressão pelo método LZW.

    O dicionário inicial é composto pelos 256 possíveis bytes.
    """

    def __init__(self):
        self.concatenacao_de_simbolos = None
        self.fluxo = None
        self.dicionario = None
        self.comprimento_codigo = None
        self.primeira_entrada = True
        self.simbolo_corrente = None

    def _int_to_bitarray(self, codigo: int) -> bitarray:
        """
        Converte um inteiro para um bitarray com o comprimento atual em bits
        do código

        :param codigo: código do dicionário
        :return: a sequência de bits relativa ao código
        :rtype: bitarray
        """
        bits = bitarray(f"{codigo:0{self.comprimento_codigo}b}")
        # if len(bits) > comprimento_maximo_codigo:
        #     raise ValueError
        return bits

    def _inicie_dicionario(self):
        """
        Inicia o dicionário de compressão com os 256 bytes iniciais
        """
        self.dicionario = dict([(bytes([x]), x) for x in range(256)])
        self.comprimento_codigo = 9

    def _atualize_dicionario_e_fluxo(self, codigo):
        self.fluxo.adicione_bits(self._int_to_bitarray(codigo))

        if len(self.dicionario) < 2 ** comprimento_maximo_codigo:
            self.dicionario[self.concatenacao_de_simbolos +
                            self.simbolo_corrente] = len(self.dicionario)
            if len(self.dicionario) == 2 ** self.comprimento_codigo:
                self.comprimento_codigo += 1
            # print(f"(*{self.comprimento_codigo})")

        print("Saída :",
              f"{codigo:0{self.comprimento_codigo}b}",
              self.dicionario[self.concatenacao_de_simbolos],
              f"'{self.concatenacao_de_simbolos}'",
              f"({len(self.dicionario)}) {self.comprimento_codigo} bits")

    def processe_de_bytes(self, sequencia: Union[bytes, str]):
        """
        Realiza a compressão da sequência de bytes, considerando que cada
        byte é um símbolo do conjunto original.

        :param sequencia: sequência de dados
        """

        # Na primeira entrada de dados: criação do dicionário padrão e mais
        # outras iniciações necessárias
        if self.primeira_entrada:
            self._inicie_dicionario()
            self.fluxo = Fluxo()
            self.concatenacao_de_simbolos = bytes([sequencia[0]])

        # Processamento da sequência de dados
        posicao = 1
        while posicao < len(sequencia):
            self.simbolo_corrente = bytes([sequencia[posicao]])
            if (self.concatenacao_de_simbolos +
                self.simbolo_corrente) in self.dicionario:
                self.concatenacao_de_simbolos += self.simbolo_corrente
            else:
                self._atualize_dicionario_e_fluxo(
                    self.dicionario[self.concatenacao_de_simbolos])
                self.concatenacao_de_simbolos = self.simbolo_corrente
                # if self.comprimento_codigo > comprimento_maximo_codigo:
                #     self._inicie_dicionario()
                #     print(">", self.dicionario[self.simbolo_corrente], len(self.dicionario))

            posicao += 1

        self.primeira_entrada = False

    def feche(self):
        """
        Encerra a entrada de dados e insere o última código no fluxo
        :return:
        """
        self._atualize_dicionario_e_fluxo(
            self.dicionario[self.concatenacao_de_simbolos])


class LZWdescompressor:
    """
    Classe para descompressão de um fluxo de bits pelo método LZW.
    
    O dicionário inicial é composto pelos 256 possíveis bytes.
    """

    def __init__(self):
        self.fluxo = Fluxo()
        self.primeira_entrada = True
        self.sequencia = None
        self.comprimento = None
        self.dicionario = None
        self._inicie_dicionario()

    def _inicie_dicionario(self):
        """
        Inicia o dicionário de descompressão com os 256 bytes iniciais
        """
        self.dicionario = dict([(x, bytes([x])) for x in range(256)])
        self.comprimento = 9

    def recupere_de_fluxo(self, fluxo: Union[bitarray, Fluxo]):
        if isinstance(fluxo, Fluxo):
            fluxo_bits = fluxo
        else:
            fluxo_bits = Fluxo()
            fluxo_bits.adicione_bits(fluxo)
        bits = fluxo_bits.obtenha_bits(self.comprimento)
        codigo_base = ba2int(bits)

        self.sequencia = self.dicionario[codigo_base]
        fim_de_fluxo = False
        while not fim_de_fluxo:
            bits = fluxo_bits.obtenha_bits(self.comprimento)
            if len(bits) == 0:
                fim_de_fluxo = True
            else:
                codigo_corrente = ba2int(bits)
                # print(f"--<{codigo_base} {codigo_corrente}>")
                # print(f"[{codigo_corrente}] {len(bits)} ", end = "")
                if len(self.dicionario):
                    a = 1  ##########################################
                if codigo_corrente in self.dicionario:
                    self.dicionario[len(self.dicionario)] = (
                            self.dicionario[codigo_base] +
                            bytes([self.dicionario[codigo_corrente][0]]))
                    # print(f"({self.dicionario[codigo_corrente]})")
                    self.sequencia += self.dicionario[codigo_corrente]
                else:
                    self.dicionario[len(self.dicionario)] = (
                            self.dicionario[codigo_base] +
                            bytes([self.dicionario[codigo_base][0]]))
                    # print(
                    #     f"{self.dicionario[codigo_base] + bytes([self.dicionario[codigo_corrente][0]])}",
                    #     self.comprimento)
                    self.sequencia += (
                            self.dicionario[codigo_base] +
                            bytes([self.dicionario[codigo_corrente][0]]))
                codigo_base = codigo_corrente
                # print(f"[{codigo_base}]", end = "")
                # print(f"({self.dicionario[codigo_base]})")

            if len(self.dicionario) == 2 ** self.comprimento - 1 and \
                    len(self.dicionario) != 2 ** comprimento_maximo_codigo - 1:
                self.comprimento += 1
                print(f"(*{self.comprimento})")

        return self.sequencia
