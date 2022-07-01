"""
Implementação de conversão de fluxo de bits para fluxo de bytes e vice-versa.

..
    Licença: GNU GENERAL PUBLIC LICENSE V.3, 2007
    Jander Moreira, 2021, 2022
"""

from bitarray import bitarray


class Fluxo:
    """
    Classe para fluxo de bits e bytes, com armazenamento interno no formato de
    bytes e bitarrays.


    """

    def __init__(self):
        self.fluxo = bitarray()

    def adicione_bits(self, sequencia: bitarray) -> None:
        """
        Adiciona bits ao fim do fluxo de bytes, transferindo bytes inteiros
        para o fluxo e os bits remanescentes em bits_final.

        :param sequencia: sequencia de bits.
        """
        self.fluxo += sequencia

    def obtenha_bits(self, comprimento: int = None) -> bitarray:
        """
        Recupera e retorna a quantidade de bits solicitada do fluxo de bits.
        Se o comprimento não for especificado, o fluxo inteiro é retornado.
        Se o fluxo estiver vazio, o retorno também é um bitarray vazio.

        :param comprimento: número de bits
        :return: os bits solicitados
        """
        if comprimento is None:
            comprimento = len(self.fluxo)
        bits = self.fluxo[:comprimento]
        self.fluxo = self.fluxo[comprimento:]
        return bits

    def obtenha_bytes(self, comprimento: int = None) -> bytes:
        """
        Recupera a quantidade de bytes solicitada, retornada como class:`bytes`,
        considerando apenas bytes "inteiros" (i.e., 8 bits). Os bits
        remanescentes permanecem no fluxo. Se o comprimento não for
        especificado, todos os bytes inteiros são retornados. Se o fluxo
        estiver vazio, o retorno também é vazio.

        :param comprimento, int: número de bytes
        :return: os bytes solicitados
        """
        if len(self.fluxo) < 8:
            sequencia_bytes = b""
        else:
            if comprimento is None:
                comprimento = len(self.fluxo)//8
            comprimento = min(comprimento, len(self.fluxo)//8)
            sequencia_bytes = self.fluxo[:comprimento * 8].tobytes()
            self.fluxo = self.fluxo[comprimento * 8:]
        return sequencia_bytes

    def limpe(self) -> None:
        """
        Limpa o fluxo de bits.
        """
        self.fluxo = bitarray()

    def __len__(self) -> int:
        """
        Retorna o comprimento do fluxo de bits.

        :return: a quantidade de bits no fluxo
        """
        return len(self.fluxo)

    def __str__(self) -> str:
        """
        Apresenta o fluxo de bytes.
        """
        numero_bytes = len(self.fluxo) // 8
        fluxo_bytes = self.fluxo[:numero_bytes * 8].tobytes()
        em_bytes = ":".join([f"{byte:02X}" for byte in fluxo_bytes])
        em_bits = "".join([str(b) for b
                           in self.fluxo[numero_bytes * 8:].tolist()])
        return f"[{em_bytes}.{em_bits}]"
