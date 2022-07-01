"""
Implementação de conversão de fluxo de bits para fluxo de bytes e vice-versa.

..
    Licença: GNU GENERAL PUBLIC LICENSE V.3, 2007
    Jander Moreira, 2021, 2022
"""

from bitarray import bitarray


class Fluxo():
    """
    Classe para fluxo de bits e bytes, com armazenamento interno no formato de
    bytes e bitarrays.


    """

    def __init__(self):
        self.fluxo_bytes = b""
        self.bits_inicio = bitarray()
        self.bits_final = bitarray()

    def adicione_bits(self, sequencia: bitarray) -> None:
        """
        Adiciona bits ao fim do fluxo de bytes, transferindo bytes inteiros
        para o fluxo e os bits remanescentes em bits_final.

        :param sequencia: sequencia de bits.
        """
        self.bits_final += sequencia
        # numero_bytes = len(self.bits_final) // 8
        # self.fluxo_bytes += self.bits_final[:numero_bytes * 8].tobytes()
        # self.bits_final = self.bits_final[numero_bytes * 8:]

    def obtenha_bits(self, comprimento) -> bitarray:
        """
        Recupera e retorna a quantidade de bits solicitada, usando os bits
        em bit_inicio e, se necessário, os do fluxo de bytes. Não havendo
        quantidade de bits suficiente, somente as contidas no fluxo são
        retornadas (caso em que a quantidade é menor que a solicitada).
        Se o fluxo estiver vazio, o retorno também é um bitarray vazio.

        :param comprimento: número de bits
        :return: os bits solicitados
        """

    def __len__(self) -> int:
        """
        Retorna o comprimento do fluxo de bits.

        :return: a quantidade de bits no fluxo
        """
        return len(self.bits_inicio) + 8 * len(self.fluxo_bytes) + \
               len(self.bits_final)

    def __str__(self):
        """
        Apresenta o fluxo de bytes.
        """
        # inicio = "".join([str(b) for b in self.bits_inicio.tolist()])
        # if len(inicio) > 0:
        #     inicio = inicio + "..."
        # fluxo = ":".join(f"{b:02X}" for b in self.fluxo_bytes)
        numero_bytes = len(self.bits_final) // 8
        self.fluxo_bytes += self.bits_final[:numero_bytes * 8].tobytes()
        final = "".join([str(b) for b in self.bits_final.tolist()])
        if len(final) > 0:
            final = "..." + final
        # return f"[{inicio}{fluxo}{final}]"
        return final