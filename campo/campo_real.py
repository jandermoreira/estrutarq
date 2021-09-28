################################################################################
################################################################################
# Campos reais

from abc import ABCMeta
from struct import pack, unpack

from estrutarq.dado import DadoBinario, DadoFixo, DadoPrefixado, DadoTerminador
from .campo_comum import CampoBasico, terminador_de_campo


################################################################################
################################################################################
# real básico
class CampoRealBasico(CampoBasico, metaclass = ABCMeta):
    """
    Classe básica para campo real
    """

    def __init__(self, tipo: str, valor: float = 0):
        super().__init__(tipo)
        self.valor = valor

    @property
    def valor(self) -> float:
        return self.__valor

    @valor.setter
    def valor(self, valor: (float, int)):
        if not isinstance(valor, (float, int)):
            raise TypeError("O valor deve ser real ou inteiro")
        self.__valor = valor

    # code::start conversoes
    def bytes_para_valor(self, dado: bytes):
        """
        Conversão de sequência de bytes com valor textual para valor real
        :param dado: sequência de 8 bytes
        """
        self.valor = float(dado)

    def valor_para_bytes(self) -> bytes:
        """
        Conversão do valor do campo para sequência de bytes textual
        :return: a sequência de bytes no padrão especificado
        """
        return bytes(f"{self.valor}", "utf-8")
    # code::end


class CampoRealFixo(DadoFixo, CampoRealBasico):
    """
    Classe para campo real com representação textual de comprimento fixo
    """

    def __init__(self, comprimento: int, **kwargs):
        CampoRealBasico.__init__(self, "real fixo", **kwargs)
        DadoFixo.__init__(self, comprimento)


class CampoRealPrefixado(DadoPrefixado, CampoRealBasico):
    """
    Classe para campo real com representação textual de comprimento fixo
    """

    def __init__(self, **kwargs):
        super().__init__("real prefixado", **kwargs)


class CampoRealTerminador(DadoTerminador, CampoRealBasico):
    """
    Classe para campo real com representação textual de comprimento fixo
    """

    def __init__(self, terminador: bytes = terminador_de_campo,
                 **kwargs):
        CampoRealBasico.__init__(self, "real fixo", **kwargs)
        DadoTerminador.__init__(self, terminador)


class CampoRealBinario(DadoBinario, CampoRealBasico):
    """
    Classe para real em formato binário usando IEEE 754 de precisão dupla
    """

    def __init__(self, **kwargs):
        CampoRealBasico.__init__(self, "real binário", **kwargs)
        DadoBinario.__init__(self, len(pack("d", 0)))

    # code::start binario_conversoes
    def bytes_para_valor(self, dado: bytes):
        """
        Conversão de sequência de bytes com representação IEEE 754 de
        precisão dupla para real
        :param dado: sequência de 8 bytes
        """
        self.valor = unpack("d", dado)[0]

    def valor_para_bytes(self) -> bytes:
        """
        Conversão do valor do campo para sequência de bytes no padrão
        IEEE 754 de precisão dupla
        :return: a sequência de bytes no padrão especificado
        """
        return pack("d", self.valor)
    # code::end
