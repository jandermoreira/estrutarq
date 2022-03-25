################################################################################
################################################################################
# Campos de cadeias de caracteres

from abc import ABCMeta
import typing

from estrutarq.dado import DadoFixo, DadoPrefixado, \
    DadoTerminador
from .campo_comum import CampoBasico, terminador_de_campo


# cadeia de caracteres básica
class CampoCadeiaBasico(CampoBasico, metaclass = ABCMeta):
    """
    Classe básica para cadeias de caracteres
    """

    def __init__(self, tipo: str, valor: str = ""):
        CampoBasico.__init__(self, tipo)
        self.valor = valor

    @property
    def valor(self):
        return self.__valor

    @valor.setter
    def valor(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError("O valor deve ser uma cadeia de caracteres")
        self.__valor = valor

    # code::start conversoes
    def bytes_para_valor(self, dado: bytes):
        """
        Atribuição de valor a partir da representação de dados
        :param dado: sequência de bytes
        """
        self.valor = dado.decode("utf-8")

    def valor_para_bytes(self) -> bytes:
        """
        Conversão da cadeia de caracteres para sequência de bytes com
        codificação UTF-8
        :return: sequência de bytes
        """
        return bytes(self.valor, "utf-8")
    # code::end


# cadeia de caracteres com terminador
class CampoCadeiaTerminador(DadoTerminador, CampoCadeiaBasico):
    """
    Classe para cadeia de caracteres com terminador
    """

    def __init__(self, **kwargs):
        CampoCadeiaBasico.__init__(self, "cadeia terminador", **kwargs)
        DadoTerminador.__init__(self, terminador_de_campo)



# cadeia de caracteres com prefixo de comprimento
class CampoCadeiaPrefixado(DadoPrefixado, CampoCadeiaBasico):
    """
    Classe para cadeia de caracteres prefixada pelo comprimento_bloco
    """

    def __init__(self, *args, **kwargs):
        CampoCadeiaBasico.__init__(self, "cadeia prefixado", *args, **kwargs)
        DadoPrefixado.__init__(self)


class CampoCadeiaFixo(DadoFixo, CampoCadeiaBasico):
    """
    Classe para cadeia de caracteres com comprimento_bloco fixo e preenchimento
    de dados inválidos
    """

    def __init__(self, comprimento: int, **kwargs):
        CampoCadeiaBasico.__init__(self, "cadeia fixo", **kwargs)
        DadoFixo.__init__(self, comprimento)

    def comprimento(self):
        """
        Obtém o comprimento_bloco do campo, se ele for fixo
        :return: o comprimento_bloco do campo se for fixo ou None se for variável
        """
        return self.comprimento
